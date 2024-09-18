import platform

import System.stdio as stdio
import System.fs as fs
import json

class Bundle:

    def __init__(self, path: str):
        if path is None:
            stdio.println("Warning: Bundle path is None.")
            return

        # If the path is a directory and contains a meta.json file
        self.path = path
        if fs.isFile(f"{path}/meta.json"):
            try:
                content = fs.reads(f"{path}/meta.json")
                metadata = json.loads(content)
                bundleType = metadata["Bundle"].split(":")[1]
                self.displayName = metadata["DisplayName"]
                self.processName = metadata["ProcessName"]
                self.description = metadata["Description"] if "Description" in metadata else ""
                self.runtimeArch = metadata["Runtime"]["SupportedArchitecture"] if "Runtime" in metadata and "SupportedArchitecture" in metadata["Runtime"] else ["universal"]
                self.bundleType = bundleType
                self.attributes = metadata["Attributes"] if "Attributes" in metadata else {}

            except Exception as e:
                stdio.println(f"It's either not a bundle or the metadata is corrupted: {e}")
                return
        else:
            stdio.println(f"Warning: Bundle path does not contain a meta.json file@{path}")
            return

    def isBundleType(self, bundleType: str) -> bool:
        return self.bundleType.lower() in bundleType.lower()

    def isArchitectureSupported(self, arch: str = None) -> bool:
        if arch is None or arch == "":
            arch = platform.uname().machine.lower()
        return arch in self.runtimeArch or "universal" in self.runtimeArch

    def isDistroSupported(self, distro: str) -> bool:
        if "Distro" in self.attributes:
            return distro.lower() in self.attributes["Distro"].lower() or "universal" in self.attributes["Distro"].lower()
        else:
            return True

    def getAttributeOf(self, key):
        if key in self.attributes:
            return self.attributes[key]
        return None

    def getExecutable(self):
        return f"{self.path}/main.py"
