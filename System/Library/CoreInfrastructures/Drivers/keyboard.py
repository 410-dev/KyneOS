import asyncio
import threading
from collections.abc import Callable

from pynput import keyboard

import System.stdio as stdio
from System.Library.CoreInfrastructures.execspaces import KernelSpace
from typing import Callable, List, Tuple

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
        "functions": []
    }


listener = None
_keySwitches: List[Tuple[List[List[keyboard.Key]], Callable]] = [
    ([[keyboard.Key.shift, keyboard.Key.f1]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 1)),
    ([[keyboard.Key.shift, keyboard.Key.f2]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 2)),
    ([[keyboard.Key.shift, keyboard.Key.f3]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 3)),
    ([[keyboard.Key.shift, keyboard.Key.f4]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 4)),
    ([[keyboard.Key.shift, keyboard.Key.f5]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 5)),
    ([[keyboard.Key.shift, keyboard.Key.f6]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 6)),
    ([[keyboard.Key.shift, keyboard.Key.f7]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 7)),
    ([[keyboard.Key.shift, keyboard.Key.f8]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 8)),
    ([[keyboard.Key.shift, keyboard.Key.f9]], lambda: KernelSpace.syscall("drv.io.tty", "switchTTY", 9))
]

def addKeySwitch(keys: list[list[keyboard.Key]], callback: Callable):
    _keySwitches.append((keys, callback))

# TODO Convert this to event handler
async def mainAsync(args: list):
    current = set()

    def on_press(key):
        try:
            current.add(key)
            for keys, callback in _keySwitches:
                if any(all(k in current for k in combination) for combination in keys):
                    callback()
                    return
        except Exception as e:
            stdio.println(f"Error: {e}")

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
    if listener is not None:
        listener.stop()

def run():
    threading.Thread(target=asyncio.run, args=(mainAsync([]),)).start()

