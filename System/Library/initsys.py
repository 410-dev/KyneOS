import datetime
import time

import System.stdio as stdio
import System.fs as fs
import System.Library.CoreInfrastructures.Enumerator.KernelSpaceLoadables as LoadableEnumerator
from System.Library.CoreInfrastructures.Objects.Process import Process
from System.Library.CoreInfrastructures.execspaces import UserSpace, KernelSpace
from System.Library.CoreInfrastructures.Objects.Bundle import Bundle

timeOfBoot: float = 0

def jPrint(string: str, end: str = "\n"):
    # Force print time as 0.00000 instead of 1e-05
    global timeOfBoot
    timeElapsed: str = f'{(datetime.datetime.now().timestamp() - timeOfBoot):.4f}'
    string = f"[{timeElapsed}] {string}"
    stdio.printf(string, end=end)

def main(args: list[str], process: Process):
    CURRENT_SYS_DISTRO = KernelSpace.getCurrentDistro()

    global timeOfBoot
    timeOfBoot = args[0]
    jPrint("Enumerating system extensions...")
    sysExtensionsEnumerated: list = LoadableEnumerator.Enumerate("Extensions", "System", CURRENT_SYS_DISTRO)
    jPrint("Enumerating system drivers...")
    sysDriversEnumerated: list = LoadableEnumerator.Enumerate("Drivers", "System", CURRENT_SYS_DISTRO)
    jPrint("Enumerating system services...")
    sysServicesEnumerated: list = LoadableEnumerator.Enumerate("Services", "System", CURRENT_SYS_DISTRO)

    jPrint("System extensions:")
    for extension in sysExtensionsEnumerated:
        jPrint(f"  {extension}")
    jPrint("System drivers:")
    for driver in sysDriversEnumerated:
        jPrint(f"  {driver}")
    jPrint("System services:")
    for service in sysServicesEnumerated:
        jPrint(f"  {service}")

    jPrint("Ordering system extensions by priority...")
    priority_max_value = 1000
    binded: list = [sysExtensionsEnumerated, sysDriversEnumerated, sysServicesEnumerated]
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
                                jPrint(
                                    f"  Warning: Priority value for {item} is greater than the maximum value ({priority_max_value}). Default set to maximum value.")
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
                            jPrint(
                                f"  Warning: Priority value for {item} is greater than the maximum value ({priority_max_value}). Default set to maximum value.")
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

    safeLocations: list[str] = [
        "/System/Services/LogonUI"
    ]

    services: list = binded[2]
    binded.pop(2)
    for idx, bind in enumerate(binded):
        if idx == 0:
            jPrint("Loading system extensions...")
        elif idx == 1:
            jPrint("Loading system drivers:")
        for item in bind:
            isBundle: bool = not item.endswith(".py")
            jPrint(f"  Loading: {item}")
            try:
                KernelSpace.load(item, args, isBundle=isBundle)
            except Exception as e:
                jPrint(f"  Error: {item}: {e}")
                jPrint("  KernelSpace failed to load the system components.")
                return 1
            jPrint(f"       OK: {item}")

    jPrint("Loading system services:")
    for bind in services:
        if "--safe" in args and bind not in safeLocations:
            jPrint(f"  [SAFE BOOT] Skipping: {bind}")
            continue
        jPrint(f"  Starting: {bind}")
        try:
            UserSpace.startService(KernelSpace._kernelUser, bind, args)
        except Exception as e:
            jPrint(f"   Error: {bind}: {e}")
            jPrint("  KernelSpace failed to load the system components.")
            return 1
        jPrint(f"        OK: {bind}")

    for drvStr in KernelSpace.loaded.keys():
        module = KernelSpace.loaded[drvStr]["exec"]
        if hasattr(module, "run"):
            try:
                module.run()
            except Exception as e:
                jPrint(f"Error in running {drvStr}: {e}")
                return 1

    while process.isRunning:
        time.sleep(0.5)
        continue
    return 0

