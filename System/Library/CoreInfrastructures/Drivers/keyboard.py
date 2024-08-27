import asyncio
import threading
from pynput import keyboard

import System.stdio as stdio
from System.Library.CoreInfrastructures.execspaces import KernelSpace

def DECLARATION() -> dict:
    return {
        "type": "drv",  # 3 letter type: ext, drv, svc
        "class": "hardwareio",
        "id": "keyboard",
        "name": "Hardware Keyboard Listener Driver",
        "version": "1.0.0",
        "description": "Virtual hardware keyboard listener driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000,
        "functions": [
            "println(str,str):None",
        ]
    }


listener = None

# TODO Convert this to event handler
async def mainAsync(args: list):
    current = set()
    ttySwitchs: dict[int, set] = {
        1: {keyboard.Key.shift, keyboard.Key.f1},
        2: {keyboard.Key.shift, keyboard.Key.f2},
        3: {keyboard.Key.shift, keyboard.Key.f3},
        4: {keyboard.Key.shift, keyboard.Key.f4},
        5: {keyboard.Key.shift, keyboard.Key.f5},
        6: {keyboard.Key.shift, keyboard.Key.f6},
        7: {keyboard.Key.shift, keyboard.Key.f7},
        8: {keyboard.Key.shift, keyboard.Key.f8},
        9: {keyboard.Key.shift, keyboard.Key.f9}
    }
    def on_press(key):
        for tty, switchKeys in ttySwitchs.items():
            if key in switchKeys:
                current.add(key)
                if all(k in current for k in switchKeys):
                    stdio.println(f"Switching to TTY {tty}")
                    KernelSpace.syscall("drv.io.tty", "switchTTY", tty)
        if key == keyboard.Key.esc:
            asyncio.run(terminateAsync(0))

    def on_release(key):
        try:
            current.remove(key)
        except KeyError:
            pass

    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    listener.join()

async def terminateAsync(code: int):
    global listener
    listener.stop()

def run():
    threading.Thread(target=asyncio.run, args=(mainAsync([]),)).start()

