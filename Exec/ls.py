from System.Library.Objects.Process import Process
import System.stdio as stdio
import System.fs as fs

def main(args: list, process: Process):
    args.pop(0)
    directory: str = " ".join(args)
    fullDir = f"{process.cwd}/{directory}"
    if directory == "":
        output = fs.listDir(process.cwd)
    elif fs.isFile(fullDir):
        stdio.println(f"{fullDir}: Not a directory")
        return 1
    elif fs.isDir(fullDir):
        if fs.accessible(fullDir, "r", process):
            output = fs.listDir(fullDir)
        else:
            stdio.println(f"{fullDir}: Permission denied")
            return 1
    else:
        stdio.println(f"{fullDir}: No such file or directory")
        return 1

    for item in output:
        stdio.println(item)
