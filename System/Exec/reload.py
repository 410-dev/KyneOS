import importlib
import sys
import re


def main(args: list, process):
    # Refresh all modules in System.*
    # Reload without restarting

    blacklist = [
        "System.Library.execspaces",
        "System.Library.initsys",
        "System.Library.kynekernel",
        "System.Library.Objects.Process",
        "*__pycache__*",
        "System.Exec.reload"
    ]

    whitelist = [
        "System.*",
        "Library.*"
    ]

    # modulesRaw = sys.modules
    # Deep copy
    modulesRaw = {}
    for module in sys.modules:
        modulesRaw[module] = sys.modules[module]

    reportFile = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "failedModules": []
    }

    for module in modulesRaw:
        if module in blacklist:
            continue

        for item in whitelist:
            if re.match(item, module):
                reportFile["total"] += 1
                try:
                    importlib.reload(modulesRaw[module])
                    reportFile["success"] += 1
                except Exception as e:
                    reportFile["failed"] += 1
                    reportFile["failedModules"].append((module, e))

    import System.stdio as stdio
    stdio.println(f"Reloaded {reportFile['success']} out of {reportFile['total']} modules.")
    if reportFile["failed"] > 0:
        stdio.println(f"Failed to reload {reportFile['failed']} modules.")
        for module, error in reportFile["failedModules"]:
            stdio.println(f"Error in {module}: {error}")
