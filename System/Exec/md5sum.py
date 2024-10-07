import hashlib
import System.stdio as stdio
import System.fs as fs

def main(args: list, process):
    args.pop(0)  # Remove the script name
    if len(args) == 0:
        stdio.println("md5: No input specified.")
        stdio.println("Usage: md5 {-S/-B} <input>")
        return 1

    # Determine input type
    if "-S" in args:
        args.remove("-S")
        if len(args) == 0:
            stdio.println("md5: No string provided for hashing.")
            stdio.println("Usage: md5 {-S/-B} <input>")
            return 1
        data = " ".join(args).encode()
    elif "-B" in args:
        args.remove("-B")
        if len(args) == 0:
            stdio.println("md5: No file path provided for hashing.")
            stdio.println("Usage: md5 {-S/-B} <input>")
            return 1
        file_path = process.cwd + "/" + " ".join(args)
        if not fs.isFile(file_path):
            stdio.println(f"md5: File not found: {' '.join(args)}")
            return 1
        data = fs.readb(file_path)
    else:
        # Default to string input if no flag is provided
        data = " ".join(args).encode()

    # Compute MD5 hash
    md5_hash = hashlib.md5(data).hexdigest()
    stdio.println(md5_hash)
    return 0
