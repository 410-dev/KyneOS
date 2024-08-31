import System.stdio as stdio
from System import fs
from System.Library.CoreInfrastructures.execspaces import UserSpace


def main(args: list, process):
    stdio.println("KyneOS Logon Interface")
    shellPrefData: dict = process.getPreferenceOf("Local:me.lks410.kyneos.kyneui")
    if shellPrefData == {}:
        process.setPreferenceOf("Local:me.lks410.kyneos.kyneui", {
            "LineFormat": "{username}@{hostname}{domain}: {cwd} $ ",
            "InitialEntryDirectory": process.ownerUser.home,
            "PATH": [
                "/Exec",
                "/Applications",
                "/System/Applications",
                "/System/Exec",
            ]
        })
        shellPrefData = process.getPreferenceOf("Local:me.lks410.kyneos.kyneui")

    hostData: dict = process.getPreferenceOf("Global:me.lks410.kyneos.machineprofile")

    process.cwd = shellPrefData["InitialEntryDirectory"] if "InitialEntryDirectory" in shellPrefData else process.ownerUser.home
    cwd = process.cwd

    while process.isRunning:
        shellPrefData = process.getPreferenceOf("Local:me.lks410.kyneos.kyneui")
        formattedLine = shellPrefData["LineFormat"]
        formattedLine = formattedLine.replace("{username}", process.ownerUser.username)
        formattedLine = formattedLine.replace("{hostname}", hostData["machineName"])
        formattedLine = formattedLine.replace("{cwd}", cwd if cwd != process.ownerUser.home else "~")
        domain = process.ownerUser.email.split("@")[1]
        if domain != "localhost":
            formattedLine = formattedLine.replace("{domain}", f"({domain})")
        else:
            formattedLine = formattedLine.replace("{domain}", "")

        stdio.printf(formattedLine, end="")
        command = stdio.scanf()

        paths: list[str] = process.ownerUser.getExecPaths()
        if command == "exit" or command == "logout":
            break
        elif command == "cd":
            cwd = process.ownerUser.home
            continue
        elif command.startswith("cd "):
            path = command.split(" ")[1]
            if path.startswith("/"):
                cwd = path
            else:
                cwd = f"{cwd}/{path}"
            continue
        elif command == "pwd":
            stdio.println(cwd)
            continue
        elif command == "paths":
            stdio.println("Paths:")
            for path in paths:
                stdio.println(f"  {path}")
            continue

        else:
            for path in paths:
                if fs.isFile(f"{path}/{command}/main.py"):
                    UserSpace.openBundle(process.ownerUser, False, f"{path}/{command}", [])
                    break
                elif fs.isFile(f"{path}/{command}.py"):
                    UserSpace.openExecutable(process.ownerUser, False, f"{path}/{command}", [])
                    break
            else:
                stdio.println(f"Command '{command}' not found")
