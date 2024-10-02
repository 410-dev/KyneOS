import System.stdio as stdio
import System.shexec as shexec


def DOWNLOAD(package_url: str, destination: str) -> tuple[bool, str]:
    # Download the package from the URL to the destination
    pass

def UNTAR(tar_file: str, destination: str) -> tuple[bool, str]:
    # Extract the tar file to the destination
    pass

def COPY(source: str, destination: str) -> tuple[bool, str]:
    # Copy the source to the destination
    pass

def REMOVE(path: str) -> tuple[bool, str]:
    # Remove the path
    pass

def RENAME(old_path: str, new_path: str) -> tuple[bool, str]:
    # Rename the old path to the new path
    pass

def SHEXEC(command: str) -> tuple[bool, str]:
    result = shexec.interpretLine(command)
    return result == 0, f"Command '{command}' failed with exit code {result}" if result != 0 else "Command executed successfully"

def IGNORE_ERROR(instruction: str) -> tuple[bool, str]:
    # Ignore the error of the instruction
    result = instructionInterpreter(instruction)
    return True, f"Ignored error: {result[1]}" if not result[0] else result[1]

def instructionInterpreter(line: str) -> tuple[bool, str]:
    # Parse the instruction
    commandComponents = line.split(" -> ")
    command = commandComponents[0]
    args = commandComponents[1:]

    # Execute the instruction
    if command == "DOWNLOAD":
        return DOWNLOAD(args[0], args[1])
    elif command == "UNTAR":
        return UNTAR(args[0], args[1])
    elif command == "COPY":
        return COPY(args[0], args[1])
    elif command == "REMOVE":
        return REMOVE(args[0])
    elif command == "RENAME":
        return RENAME(args[0], args[1])
    elif command == "SHEXEC":
        return SHEXEC(args[0])
    elif command == "IGNORE_ERROR":
        return IGNORE_ERROR(args[0])
    else:
        return False, "Invalid command"
