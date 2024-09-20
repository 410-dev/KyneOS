# This file should rewrite as new call of /System/Exec/framework
from os.path import split

import System.shexec as shell

def main(args: list[str], process):
    args.pop(0)

    executable: str = args[0].split("://")[1].split("?")[0]
    execArgs: str = ""
    if "?" in args[0] and not args[0].endswith("?"):
        execArgs = args[0].split("?", 1)[1]

    argsDict: dict[str, str] = {}
    execArgs: list = execArgs.split("&")
    for element in execArgs:
        splitted: list[str] = element.split("=", 1)
        if len(splitted) < 2:
            argsDict[splitted[0]] = ""
        else:
            argsDict[splitted[0]] = "=".join(splitted[1:])

    targetFile = argsDict.get("file")
    newargs = argsDict.get("args")

    return shell.interpretLine(f'"{executable}" {targetFile} {newargs}', process)
