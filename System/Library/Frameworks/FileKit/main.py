# This file should rewrite as new call of /System/Exec/framework

import System.shexec as shell
import System.stdio as stdio
import System.url as urlParser

def main(args: list, process):
    newCallCmd: list[str] = [
        "/System/Exec/framework",
        "/System/Library/Frameworks/FileKit"
    ]

    args.pop(0)

    if len(args) == 0:
        stdio.println("FileKit: No URL specified.")
        return 1

    if args[0] == "--silent":
        args.pop(0)

    protocol, url, args = urlParser.decodeURLByComponents(args[0])

    newCallCmd.append(f"path={url}")
    for key, value in args.items():
        newCallCmd.append(f"{key}={value}")

    return shell.interpretParameters(newCallCmd, process)
