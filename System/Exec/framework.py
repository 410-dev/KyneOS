import System.framework as framework
import System.stdio as stdio

def main(args: list, process):
    # First arg: Framework file
    # Second arg: Parameters in like this: abc=1234 def=5678
    args.pop(0)
    if len(args) < 1:
        stdio.println("Usage: framework [--silent] [frameworkfile] <args>")
        stdio.println("       framework [--silent] [url form]")
        stdio.println("Example: framework /System/Library/Frameworks/FileKit arg1=123 arg2=456")
        stdio.println("         framework --silent /System/Library/Frameworks/FileKit?arg1=123&arg2=456")
        return 1

    silent: bool = False
    if args[0] == "--silent":
        args.pop(0)
        silent = True

    frameworkFile: str = args.pop(0)
    if "?" in frameworkFile:
        frameworkFile, params = frameworkFile.split("?", 1)
        args.extend(params.split("&"))
    try:
        castedParameters: dict = {}
        unidentifiedIdx: int = 0
        for parameter in args:
            if "=" not in parameter:
                key = f"unnamedParameter_{unidentifiedIdx}"
                value = parameter
            else:
                key, value = parameter.split("=", 1)
            castedParameters[key] = value
        # When resource is requested, return the resource data
        if "resource" in castedParameters:
            requestedResources: list[str] = castedParameters["resource"].split(",")
            resourceData: dict = {}
            try:
                resourceData = framework.getFrameworkResource(frameworkFile, process, requestedResources)
            except Exception as e:
                stdio.println(f"Error: {e}")

            if "encode" in castedParameters:
                if castedParameters["encode"] == "base64":
                    import base64
                    for resource in resourceData:
                        if isinstance(resourceData[resource], str):
                            resourceData[resource] = base64.b64encode(resourceData[resource].encode()).decode()
                        else:
                            resourceData[resource] = base64.b64encode(resourceData[resource]).decode()

            return resourceData

        # If not asking for resource, run the framework
        else:
            output = framework.run(frameworkFile, castedParameters, process)
            if not silent:
                stdio.println(output)
            return output
    except Exception as e:
        stdio.println(f"Error: {e}")
        return 1
