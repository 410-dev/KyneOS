import System.stdio as stdio
import System.framework as framework
import System.url as url

def main(args: dict, process):
    if "task" not in args:
        return "Error: No task specified"

    if args["task"] == "install":
        # Installing NanoPyOS backend to system
        if not process.ownerUser.isAdministrator():
            return "Error: Installation requires administrator privileges."

        # Requires parameter: usingInternal
        if "usingInternal" not in args:
            return "Error: No usingInternal specified"

        # If lowercased usingInternal is not "true", require manifest parameter
        if args["usingInternal"].lower() != "true":
            if "manifest" not in args:
                return "Error: Non-internal installation requires manifest path to be specified."

        # If usingInternal is true, install from internal path
        if args["usingInternal"].lower() == "true":
            # Install from internal path
            packageManifest = "file:///System/Library/Frameworks/NanoPyOSBackend/resources/manifest.json?as=text"
        else:
            # Install from specified path
            packageManifest = args["manifest"]

        # Install package
        stdio.println("Installing NanoPyOS Backend...")
        stdio.println(f"Package manifest: {packageManifest}")
        stdio.println(f"Reading package manifest....")
        manifestData = url.retrieve(packageManifest, process)

        # stdio.println(f"{manifestData}")
