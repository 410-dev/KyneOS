from System.Library.execspaces import KernelSpace

import System.stdio as stdio

def main(args: list[str], process):
    args.pop(0)
    if len(args) == 0:
        stdio.println("Usage: open <file>")
        return 1

    file = args.pop(0)
    associations = process.ownerUser.getPreferenceOf("me.lks410.associations")
    fileExt = file.split(".")[-1]
    if fileExt in associations:
        association = associations[fileExt]["assoc"]
    else:
        stdio.println(f"Error: No association found for {fileExt}")
        return 1

    url = f"{association}?file={file}&args={','.join(args)}"

    return KernelSpace.syscall("ext.sys.urlcalls", "call", url, process)
