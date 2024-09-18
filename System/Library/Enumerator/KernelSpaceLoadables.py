import System.fs as fs
import System.stdio as stdio

from System.Library.Objects.Bundle import Bundle
from System.Library.Objects.User import User

# This will return a list of bundles that match the scope and distro.
# It will return as absolute path from root device (pwd in host)
def Enumerate(namespace: str, scope: str, distro: str, user: User = None) -> list[str]:
    # Distro could be Server / Desktop / Universal.
    # Server: Only runs server distribution system.
    # Desktop: Only runs desktop distribution system.
    # Universal: Runs both server and desktop distribution system.

    # Scope could be System / Kernel / User@#### where #### is the user ID.

    # By scope first
    traversePaths: list[str] = []
    if scope == "System":
        traversePaths.append(f"/System/{namespace}")
        traversePaths.append(f"/Library/{namespace}")
        if distro == "Server":
            traversePaths.append(f"/System/Server/{namespace}")
            traversePaths.append(f"/Library/Server/{namespace}")
    elif scope == "Kernel":
        traversePaths.append(f"/System/Library/{namespace}")
        if distro == "Server":
            traversePaths.append(f"/System/Library/ServerInfrastructures/{namespace}")
    elif scope == "User":
        if user is None:
            raise Exception("User scope requires user object.")

        if namespace == "Drivers":
            raise Exception("User scope cannot load drivers.")

        userHome = user.home
        traversePaths.append(f"{userHome}/Library/{namespace}")
    else:
        raise Exception(f"Unknown scope: {scope}")

    # Now traverse the paths and return the list of loadables
    loadables: list[str] = []
    for path in traversePaths:
        if fs.isDir(path):
            files: list[str] = fs.listDir(path)
            for file in files:
                # Skip disabled loadables
                if ".disabled" in file:
                    continue
                if file.startswith(".") or file.startswith("_"):
                    continue

                # Single script file
                if file.endswith(".py"):
                    loadables.append(f"{path}/{file}")

                # Bundle
                elif fs.isDir(f"{path}/{file}") and fs.isFile(f"{path}/{file}/meta.json"):
                    try:
                        bundle = Bundle(f"{path}/{file}")
                        if bundle.isBundleType(f"{namespace}") and bundle.isDistroSupported(distro):
                            if bundle.getAttributeOf("Enabled") is not None and not bundle.getAttributeOf("Enabled"):
                                stdio.println(f"  Bundle {path}/{file} is disabled. Skipping.")
                                continue
                            loadables.append(f"{path}/{file}")
                    except Exception as e:
                        stdio.println("Warning: Non-bundle directory found. Skipping.")
                        continue

    return loadables
