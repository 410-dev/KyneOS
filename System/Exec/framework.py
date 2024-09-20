import System.framework as framework
import System.stdio as stdio

def main(args: list, process):
    # First arg: Framework file
    # Second arg: Parameters in like this: abc=1234 def=5678
    args.pop(0)
    if len(args) < 1:
        stdio.println("Usage: framework [frameworkfile] <args>")
        stdio.println("Example: framework /System/Library/Frameworks/FileKit arg1=123 arg2=456")
        return 1

    frameworkFile: str = args.pop(0)
    try:
        castedParameters: dict = {}
        for parameter in args:
            key, value = parameter.split("=", 1)
            castedParameters[key] = value
        output = framework.run(frameworkFile, castedParameters, process)
        stdio.println(output)
    except Exception as e:
        stdio.println(f"Error: {e}")
        return 1
    return 0
