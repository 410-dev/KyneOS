# This file is called by /System/Exec/framework

import System.shexec as shell
import System.fs as fs
import random

def main(args: dict, process):
    randomString = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(8)])

    handling = f"capture-output filekit-{randomString} run-silently cat %file%"
    if "as" in args.keys():
        returnTypeSupported = {
            "text": f"capture-output filekit-{randomString} run-silently cat %file%",
            "b64s": f"capture-output filekit-{randomString} run-silently b64 encode %file%",
            "b64b": f"capture-output filekit-{randomString} run-silently b64 encode -B %file%",
        }
        handling = returnTypeSupported[args["as"]]

    handling = handling.replace("%file%", args["path"])
    shell.interpretLine(handling, process)
    dataOutput = fs.reads(f"/tmp/capture-output/filekit-{randomString}.txt")
    fs.remove(f"/tmp/capture-output/filekit-{randomString}.txt")
    return dataOutput


