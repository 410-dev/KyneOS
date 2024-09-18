import asyncio
import sys
import datetime
import threading
import time

import System.stdio as stdio
import System.fs as fs

import System.Library.initsys as initsys
import System.Library.Enumerator.KernelSpaceLoadables as LoadableEnumerator
from System.Library.Objects.Process import Process

from System.Library.execspaces import KernelSpace
from System.Library.Objects.Bundle import Bundle

CURRENT_SYS_DISTRO = "Desktop"
CURRENT_KRNL_NAME = "Kyne"
CURRENT_KRNL_VERSION = "1.0.0"
CURRENT_KRNL_TESTVRS = "alpha 1"

timeOfBoot: float = datetime.datetime.now().timestamp()
preloadInitialized: bool = False

def jPrint(string: str, end: str = "\n"):
    # Force print time as 0.00000 instead of 1e-05
    timeElapsed: str = f'{(datetime.datetime.now().timestamp() - timeOfBoot):.4f}'
    string = f"[{timeElapsed}] {string}"
    if preloadInitialized:
        stdio.printf(string, end=end)
    else:
        print(string, end=end)

def killsys():
    import sys
    import os
    currentPid = os.getpid()
    time.sleep(3)
    if sys.platform == "win32":
        # silently kill the process using taskkill
        os.system(f"taskkill /F /PID {currentPid}")
    else:
        os.system(f"kill -9 {currentPid}")

def init(args: list):
    global CURRENT_SYS_DISTRO
    if "--distro=s" in args:
        CURRENT_SYS_DISTRO = "Server"
        KernelSpace._currentDistro = "Server"
    elif "--distro=d" in args:
        CURRENT_SYS_DISTRO = "Desktop"
        KernelSpace._currentDistro = "Desktop"
    else:
        CURRENT_SYS_DISTRO = "Desktop"
        KernelSpace._currentDistro = "Desktop"
    KernelSpace._bootArgs = args
    jPrint(f"{CURRENT_KRNL_NAME} {CURRENT_KRNL_VERSION} {CURRENT_KRNL_TESTVRS} Kernel - {CURRENT_SYS_DISTRO}")
    formattedCurrentTime: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jPrint(f"Startup at: {formattedCurrentTime}")
    jPrint(f"Initialization parameters: {' '.join(args)}")

    # Clear kernelSpace
    jPrint("Initializing kernel space...")
    KernelSpace.loaded.clear()

    # Import file system and output driver
    jPrint("Loading preload components for next process...")
    preloadList: list[tuple[str, bool]] = [
        ("/System/Library/Extensions/kfs.py", False),
        ("/System/Library/Extensions/directories.py", False),
        ("/System/Library/Drivers/tty.py", False),
        ("/System/Library/Drivers/stdout.py", False),
    ]
    for preload in preloadList:
        jPrint(f"Loading: {preload[0]}")
        try:
            KernelSpace.load(preload[0], args, isBundle=preload[1])
        except Exception as e:
            jPrint(f"  Error: {preload[0]}: {e}")
            jPrint("  KernelSpace failed to load the preload components.")
            sys.exit(1)
        jPrint(f"     OK: {preload[0]}")
    global preloadInitialized
    preloadInitialized = True
    jPrint("Preload components loaded.")

    if "--dont-clean-tmp" not in args:
        jPrint("Cleaning temporary files...")
        fs.remove("/tmp")
        fs.makeDir("/tmp")

    # Load
    jPrint("Enumerating kernel extensions...")
    kernelExtensionsEnumerated: list = LoadableEnumerator.Enumerate("Extensions", "Kernel", CURRENT_SYS_DISTRO)
    jPrint("Enumerating kernel drivers...")
    kernelDriversEnumerated: list = LoadableEnumerator.Enumerate("Drivers", "Kernel", CURRENT_SYS_DISTRO)
    # jPrint("Enumerating kernel services...")
    # kernelServicesEnumerated: list = LoadableEnumerator.Enumerate("Services", "Kernel", CURRENT_SYS_DISTRO)

    for preload in preloadList:
        if preload[0] in kernelExtensionsEnumerated:
            kernelExtensionsEnumerated.remove(preload[0])
        if preload[0] in kernelDriversEnumerated:
            kernelDriversEnumerated.remove(preload[0])
        if preload[0] in kernelServicesEnumerated:
            kernelServicesEnumerated.remove(preload[0])

    jPrint("Kernel extensions:")
    for extension in kernelExtensionsEnumerated:
        jPrint(f"  {extension}")
    jPrint("Kernel drivers:")
    for driver in kernelDriversEnumerated:
        jPrint(f"  {driver}")
    jPrint("Kernel services:")
    for service in kernelServicesEnumerated:
        jPrint(f"  {service}")

    safeLocations: list[str] = [
        "/System/Library/Drivers/keyboard.py",
        "/System/Library/Drivers/stdin.py",
        "/System/Library/Drivers/stdout.py",
        "/System/Library/Drivers/tty.py",
        "/System/Library/Extensions/AuthMan",
        "/System/Library/Extensions/directories.py",
        "/System/Library/Extensions/display.py",
        "/System/Library/Extensions/dsParser.py",
        "/System/Library/Extensions/kfs.py"
    ]

    jPrint("Ordering kernel extensions by priority...")
    priority_max_value = 1000
    binded: list = [kernelExtensionsEnumerated, kernelDriversEnumerated, kernelServicesEnumerated]
    for bind in binded:
        ordered: list[tuple[int, str]] = []
        for item in bind:
            try:
                if item.endswith(".py"):
                    data = fs.reads(item)
                    data = data.split("\n")
                    foundPriority: bool = False
                    for line in data:
                        line = line.strip()
                        line = line.replace(",", "").replace(" ", "").replace("\"", "")
                        if line.startswith("#Priority:") or line.startswith("priority:"):
                            lineComponent = line.split(":")
                            priority = int(lineComponent[1])
                            if priority > priority_max_value:
                                jPrint(f"  Warning: Priority value for {item} is greater than the maximum value ({priority_max_value}). Default set to maximum value.")
                                priority = priority_max_value
                            ordered.append((priority, item))
                            foundPriority = True
                            break
                    if not foundPriority:
                        jPrint(f"  Warning: Priority not found for {item}. Default set to lowest priority (0).")
                        ordered.append((0, item))
                else:
                    bundle: Bundle = Bundle(item)
                    priorityInt: int = bundle.getAttributeOf("Priority")
                    if priorityInt is not None:
                        if priorityInt > priority_max_value:
                            jPrint(f"  Warning: Priority value for {item} is greater than the maximum value ({priority_max_value}). Default set to maximum value.")
                            priorityInt = priority_max_value
                        ordered.append((priorityInt, item))
                    else:
                        jPrint(f"  Warning: Priority not found for {item}. Default set to lowest priority (0).")
                        ordered.append((0, item))

            except Exception as e:
                jPrint(f"  Error: Failed to read priority of {item}: {e}")
                jPrint(f"       : Default set to lowest priority (0).")
                ordered.append((0, item))
        ordered.sort(key=lambda x: x[0], reverse=True)
        bind.clear()
        for item in ordered:
            bind.append(item[1])

    # services: list = binded[2]
    binded.pop(2)
    for idx, bind in enumerate(binded):
        if idx == 0:
            jPrint("Loading kernel extensions...")
        elif idx == 1:
            jPrint("Loading kernel drivers:")
        for item in bind:
            if "--safe" in args and item not in safeLocations:
                jPrint(f"  [SAFE BOOT] Skipping: {item}")
                continue
            isBundle: bool = not item.endswith(".py")
            jPrint(f"  Loading: {item}")
            try:
                KernelSpace.load(item, args, isBundle=isBundle)
            except Exception as e:
                jPrint(f"  Error: {item}: {e}")
                jPrint("  KernelSpace failed to load the kernel components.")
                sys.exit(1)
            jPrint(f"       OK: {item}")

    # jPrint("Loading kernel services:")
    # for bind in services:
    #     if "--safe" in args and bind not in safeLocations:
    #         jPrint(f"  [SAFE BOOT] Skipping: {bind}")
    #         continue
    #     jPrint(f"  Starting: {bind}")
    #     try:
    #         KernelSpace.startService(bind, args)
    #     except Exception as e:
    #         jPrint(f"   Error: {bind}: {e}")
    #         jPrint("  KernelSpace failed to load the kernel components.")
    #         sys.exit(1)
    #     jPrint(f"        OK: {bind}")

    initProcess: Process = Process("init", "/System/Library/initsys.py", args, KernelSpace._kernelUser)
    args = [timeOfBoot] + args
    initProcess.launchSync(args)

    for loadedKernelServices in KernelSpace.serviceProcesses:
        jPrint(f"Terminating service: {loadedKernelServices}")
        service: Process = KernelSpace.serviceProcesses[loadedKernelServices]
        try:
            service.kill(0)
            jPrint(f"     OK: {loadedKernelServices}")
        except Exception as e:
            jPrint(f"  Error: {loadedKernelServices}: {e}")
            jPrint("  KernelSpace failed to terminate the kernel services.")

    for loadedKernelComponents in KernelSpace.loaded:
        jPrint(f"Unloading: {loadedKernelComponents}")
        module = KernelSpace.loaded[loadedKernelComponents]["exec"]
        if hasattr(module, "terminate"):
            try:
                jPrint("  Terminating...")
                module.terminate(0)
            except Exception as e:
                jPrint(f"  Error: {loadedKernelComponents}: {e}")
                jPrint("  KernelSpace failed to terminate the kernel components.")
                sys.exit(1)
        if hasattr(module, "terminateAsync"):
            try:
                jPrint("  Terminating async...")
                threading.Thread(target=asyncio.run, args=(module.terminateAsync(0),)).start()
            except Exception as e:
                jPrint(f"  Error: {loadedKernelComponents}: {e}")
                jPrint("  KernelSpace failed to terminate the kernel components.")
                sys.exit(1)

        jPrint(f"     OK: {loadedKernelComponents}")
    jPrint("Kernel components unloaded.")
    jPrint("Kernel shutdown complete.")
    killsys()
