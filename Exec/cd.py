from System.Library.CoreInfrastructures.Objects.Process import Process
import System.stdio as stdio
import System.fs as fs

def main(args: list, process: Process):
    args.pop(0)
    directory: str = " ".join(args)
    parentProcess: Process = process.ownerProcess
    if directory == "":
        parentProcess.cwd = parentProcess.ownerUser.home
        return
    if directory.startswith("/"):
        nextDir = directory
    else:
        nextDir = f"{parentProcess.cwd}/{directory}"

    if fs.isFile(nextDir):
        stdio.println(f"{directory}: Not a directory")
        return 1
    if fs.isDir(nextDir):
        if fs.accessible(nextDir, "x", process):
            parentProcess.cwd = nextDir
            return 0
        stdio.println(f"{directory}: Permission denied")
    stdio.println(f"{directory}: No such file or directory")
    return 1