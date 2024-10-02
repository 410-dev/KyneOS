import System.Library.kynekernel as kernelfile
import System.stdio as stdio
from System.Library.Objects.Bundle import Bundle

def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "sys",
        "id": "profile",
        "name": "System Profiler",
        "version": "1.0.0",
        "description": "System Profiler Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

currentBundle: Bundle = Bundle("/System/Library/Frameworks/OSProfiler")
properties = currentBundle.getAttributeOf("ExplicitCompatibility")

if "OSDistro" in properties.keys():
    if properties["OSDistro"] != "Automatic":
        allowedDistros = ["Desktop", "Server"]
        if properties["OSDistro"] in allowedDistros:
            kernelfile.CURRENT_SYS_DISTRO = properties["OSDistro"]
            stdio.println(f"OSDistro set to {properties['OSDistro']}")
        else:
            stdio.println(f"WARNING: OSDistro is set to {properties['OSDistro']} which is not allowed. Leaving as-is: {kernelfile.CURRENT_SYS_DISTRO}")
    else:
        stdio.println(f"OSDistro set to Automatic. Leaving as-is: {kernelfile.CURRENT_SYS_DISTRO}")
else:
    stdio.println("WARNING: No OSDistro specified in OSProfiler.")
