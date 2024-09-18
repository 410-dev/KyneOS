from System.Library.Objects.Process import Process
import System.stdio as stdio
import System.fs as fs

def main(args: list, process: Process):
    args.pop(0)
    file: str = " ".join(args)
    if file.startswith("/"):
        path = file
    elif file.startswith("~"):
        path = f"{process.ownerUser.home}/{file[1:]}"
    else:
        path = f"{process.cwd}/{file}"

    if fs.accessible(path, "r", process):
        content = fs.reads(path)
        stdio.println(content)
        return 0
