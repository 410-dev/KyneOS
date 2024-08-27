import inspect

import System.fs as fs
from System.Library.CoreInfrastructures.Objects.Process import Process
from System.Library.CoreInfrastructures.execspaces import KernelSpace


def DECLARATION() -> dict:
    return {
        "type": "drv",
        "class": "io",
        "id": "tty",
        "name": "tty",
        "version": "1.0.0",
        "description": "Multiple display TTY driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

currentDisplayTTY = 1

scanfQueue: dict[int, bool] = {}

def switchTTY(tty: int):
    global currentDisplayTTY
    currentDisplayTTY = tty
    from System.Library.CoreInfrastructures.execspaces import KernelSpace
    if not fs.isFile(f"/tmp/tty{tty}.log"):
        fs.makeDir(f"/tmp/")
        fs.writes(f"/tmp/tty{tty}.log", "")
    KernelSpace.syscall("ext.vhardware.stddisplay", "clear")
    println(f"Switched to TTY {tty}", tty=tty, dontLeaveLog=True)
    print(fs.reads(f"/tmp/tty{tty}.log"))

def scanf(tty: int = -1) -> str:
    global scanfQueue
    if tty == -1:
        tty = currentDisplayTTY
    if tty not in scanfQueue:
        scanfQueue[tty] = False
    if scanfQueue[tty]:
        return ""
    scanfQueue[tty] = True
    return input()

def println(content: str, end: str = "\n", tty: int = -1, dontLeaveLog: bool = False, enableTTYDetection: bool = True):
    global currentDisplayTTY
    if tty == -1:
        if enableTTYDetection:
            stack = inspect.stack()
            for frame_info in stack:
                frame_locals = frame_info.frame.f_locals
                if 'self' in frame_locals:
                    caller_self = frame_locals['self']

                    if isinstance(caller_self, Process):
                        tty = caller_self.assignedTTY
                        break
        else:
            tty = currentDisplayTTY

    if tty == currentDisplayTTY:
        print(content, end=end)

    if not dontLeaveLog:
        fs.appends(f"/tmp/tty{tty}.log", content + end)
