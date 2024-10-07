import hashlib
import System.stdio as stdio
import System.fs as fs

def main(args: list, process):
    args.pop(0)  # Remove the script name
    if len(args) < 2:
        stdio.println("sha: Insufficient arguments.")
        stdio.println("Usage: sha <256/512> {-S/-B} <input>")
        return 1

    # Extract SHA variant
    sha_variant = args.pop(0)
    if sha_variant not in ["256", "512"]:
        stdio.println(f"sha: Unsupported SHA variant '{sha_variant}'. Supported variants: 256, 512.")
        return 1

    # Determine input type
    if "-S" in args:
        args.remove("-S")
        if len(args) == 0:
            stdio.println("sha: No string provided for hashing.")
            stdio.println("Usage: sha <256/512> {-S/-B} <input>")
            return 1
        data = " ".join(args).encode()
    elif "-B" in args:
        args.remove("-B")
        if len(args) == 0:
            stdio.println("sha: No file path provided for hashing.")
            stdio.println("Usage: sha <256/512> {-S/-B} <input>")
            return 1
        file_path = process.cwd + "/" + " ".join(args)
        if not fs.isFile(file_path):
            stdio.println(f"sha: File not found: {' '.join(args)}")
            return 1
        data = fs.readb(file_path)
    else:
        # Default to string input if no flag is provided
        data = " ".join(args).encode()

    # Select the appropriate SHA function
    if sha_variant == "256":
        sha_hash = hashlib.sha256(data).hexdigest()
    elif sha_variant == "512":
        sha_hash = hashlib.sha512(data).hexdigest()

    stdio.println(sha_hash)
    return 0
