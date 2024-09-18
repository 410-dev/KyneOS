from System.Library.CoreInfrastructures.Objects.Process import Process
from System.Library.CoreInfrastructures.execspaces import UserSpace
import System.stdio as stdio
import System.fs as fs

def paths(process: Process) -> list[str]:
    return process.ownerUser.getExecPaths()


def interpretLine(line: str, process: Process) -> int:
    if "; " in line:
        lines: list[str] = line.split("; ")
        return interpretLines(lines, process)
    commandComponents: list[str] = splitStringBySpaceWhileConsideringEscapeAndQuotation(line)
    return interpretParameters(commandComponents, process)


def interpretLines(lines: list[str], process: Process) -> int:
    for line in lines:
        exitCode: int = interpretLine(line, process)
        if exitCode != 0:
            return exitCode
    return 0


def interpretParameters(commandComponents: list[str], process: Process) -> int:
    for path in paths(process):
        try:
            if fs.isFile(f"{path}/{commandComponents[0]}/main.py"):
                return UserSpace.openBundle(process.ownerUser, False, f"{path}/{commandComponents[0]}", commandComponents, process.cwd)
            elif fs.isFile(f"{path}/{commandComponents[0]}.py"):
                return UserSpace.openExecutable(process.ownerUser, False, f"{path}/{commandComponents[0]}", commandComponents, process.cwd)
        except Exception as e:
            stdio.println(f"Error: {e}")
            return 2
    else:
        stdio.println(f"Command '{commandComponents[0]}' not found")
        return 1


def splitStringBySpaceWhileConsideringEscapeAndQuotation(rawStringLine: str) -> list[str]:
    splitLine: list[str] = []
    currentString: str = ""
    inEscape: bool = False
    inQuotation: bool = False
    for char in rawStringLine:
        if inEscape:
            currentString += char
            inEscape = False
            continue
        if char == "\\":
            inEscape = True
            continue
        if char == "\"":
            inQuotation = not inQuotation
            continue
        if char == " " and not inQuotation:
            splitLine.append(currentString)
            currentString = ""
            continue
        currentString += char
    splitLine.append(currentString)
    return splitLine
