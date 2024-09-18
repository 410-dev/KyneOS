from System.Library.CoreInfrastructures.Objects.Process import Process
import System.stdio as stdio
import System.fs as fs

def main(args: list, process: Process):
    args.pop(0)
    directory: str = " ".join(args)
    if directory.startswith("/"):
        parentDir = directory
        fullDir = directory
    elif directory.startswith("~"):
        parentDir = process.ownerUser.home
        fullDir = f"{process.ownerUser.home}/{directory[1:]}"
    else:
        parentDir = process.cwd
        fullDir = f"{process.cwd}/{directory}"

    if fs.accessible(parentDir, "w", process):
        if fs.makeDir(fullDir):
            return 0
        stdio.println(f"mkdir: cannot create directory '{fullDir}': File exists")
        return 1
