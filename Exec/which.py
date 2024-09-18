import System.shexec as shexec
import System.fs as fs
import System.stdio as stdio

def main(args: list[str], process):
    args.pop(0)
    for path in shexec.paths(process):
        try:
            if fs.isFile(f"{path}/{args[0]}/main.py"):
                stdio.println(f"{path}/{args[0]}")
                return 0
            elif fs.isFile(f"{path}/{args[0]}.py"):
                stdio.println(f"{path}/{args[0]}")
                return 0
        except Exception as e:
            stdio.println(f"Error: {e}")
            return 2
    else:
        stdio.println(f"Command '{args[0]}' not found")
        return 1
