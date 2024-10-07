

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "setup",
        "id": "defaultusermaker",
        "name": "KyneOS Time Manager",
        "version": "1.0.0",
        "description": "KyneOS Time Manager Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }

import sys
from pynput import keyboard
import System.syscall as KernelSpace
import System.Library.kynekernel as kynekernel

# def killsys():
#     import sys
#     import os
#     currentPid = os.getpid()
#     if sys.platform == "win32":
#         os.system(f"taskkill /F /PID {currentPid}")
#     else:
#         os.system(f"kill -9 {currentPid}")

KernelSpace.syscall("drv.hardwareio.keyboard", "addKeySwitch", [[keyboard.Key.ctrl, keyboard.Key.esc]], lambda: kynekernel.killsys())
