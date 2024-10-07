import base64
import System.stdio as stdio
import System.fs as fs

def main(args: list, process):
    args.pop(0)
    if len(args) == 0:
        stdio.println("b64: No input specified.")
        stdio.println("Usage: b64 encode/decode {-S/-B} <input>")
        return 1

    if args[0] == "encode":
        args.pop(0)
        if "-S" in args:
            args.remove("-S")
            dat = " ".join(args)
        elif "-B" in args:
            args.remove("-B")
            if not fs.isFile(process.cwd + "/" + " ".join(args)):
                stdio.println(f"b64: File not found: {' '.join(args)}")
                return 1
            dat = fs.readb(process.cwd + "/" + " ".join(args))
        else:
            if not fs.isFile(process.cwd + "/" + " ".join(args)):
                stdio.println(f"b64: File not found: {' '.join(args)}")
                return 1
            dat = fs.reads(process.cwd + "/" + " ".join(args))

        stdio.println(base64.b64encode(dat.encode()).decode())
    elif args[0] == "decode":
        args.pop(0)
        if "-S" in args:
            args.remove("-S")
            dat = " ".join(args)
        elif "-B" in args:
            args.remove("-B")
            if not fs.isFile(process.cwd + "/" + " ".join(args)):
                stdio.println(f"b64: File not found: {' '.join(args)}")
                return 1
            dat = fs.readb(process.cwd + "/" + " ".join(args))
        else:
            if not fs.isFile(process.cwd + "/" + " ".join(args)):
                stdio.println(f"b64: File not found: {' '.join(args)}")
                return 1
            dat = fs.reads(process.cwd + "/" + " ".join(args))

        try:
            stdio.println(base64.b64decode(dat).decode())
        except:
            stdio.println("b64: Invalid base64 data.")
            return 1

    else:
        stdio.println("base64: Invalid option.")
        stdio.println("Usage: b64 encode/decode {-S/-B} <input>")
        return 1

    return 0
