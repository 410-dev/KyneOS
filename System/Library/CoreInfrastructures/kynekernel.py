import sys
import datetime
import System.stdio as stdio
import System.fs as fs

import System.Library.initsys as initsys
import System.Library.CoreInfrastructures.Enumerator.KernelSpaceLoadables as LoadableEnumerator
from System.Library.CoreInfrastructures.Objects.Process import Process

from System.Library.CoreInfrastructures.execspaces import KernelSpace
from System.Library.CoreInfrastructures.Objects.Bundle import Bundle

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

def init(args: list):
    global CURRENT_SYS_DISTRO
    if "--distro=s" in args:
        CURRENT_SYS_DISTRO = "Server"
    elif "--distro=d" in args:
        CURRENT_SYS_DISTRO = "Desktop"
    else:
        CURRENT_SYS_DISTRO = "Desktop"
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
        ("/System/Library/CoreInfrastructures/Extensions/kfs.py", False),
        ("/System/Library/CoreInfrastructures/Extensions/directories.py", False),
        ("/System/Library/CoreInfrastructures/Drivers/tty.py", False),
        ("/System/Library/CoreInfrastructures/Drivers/stdout.py", False),
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

    # Load
    jPrint("Enumerating kernel extensions...")
    kernelExtensionsEnumerated: list = LoadableEnumerator.Enumerate("Extensions", "Kernel", CURRENT_SYS_DISTRO)
    jPrint("Enumerating kernel drivers...")
    kernelDriversEnumerated: list = LoadableEnumerator.Enumerate("Drivers", "Kernel", CURRENT_SYS_DISTRO)
    jPrint("Enumerating kernel services...")
    kernelServicesEnumerated: list = LoadableEnumerator.Enumerate("Services", "Kernel", CURRENT_SYS_DISTRO)

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

    services: list = binded[2]
    binded.pop(2)
    for idx, bind in enumerate(binded):
        if idx == 0:
            jPrint("Loading kernel extensions...")
        elif idx == 1:
            jPrint("Loading kernel drivers:")
        for item in bind:
            isBundle: bool = not item.endswith(".py")
            jPrint(f"  Loading: {item}")
            try:
                KernelSpace.load(item, args, isBundle=isBundle)
            except Exception as e:
                jPrint(f"  Error: {item}: {e}")
                jPrint("  KernelSpace failed to load the kernel components.")
                sys.exit(1)
            jPrint(f"       OK: {item}")

    jPrint("Loading kernel services:")
    for bind in services:
        jPrint(f"  Starting: {bind}")
        try:
            KernelSpace.startService(bind, args)
        except Exception as e:
            jPrint(f"   Error: {bind}: {e}")
            jPrint("  KernelSpace failed to load the kernel components.")
            sys.exit(1)
        jPrint(f"        OK: {bind}")

    # from System.Library.CoreInfrastructures.Objects.DSObject import DSObject
    # dobj = DSObject("/Example/google.com/Human Resources/HR Managers")
    # jPrint(dobj.getName())
    # jPrint(dobj.__str__())

    initProcess: Process = Process("init", "/System/Library/initsys.py", args, KernelSpace._kernelUser)
    args = [timeOfBoot] + args
    initProcess.launchSync(args)
