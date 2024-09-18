import System.stdio as stdio
import System.shexec as shell
from System import fs
from System.Library.execspaces import UserSpace


def main(args: list, process):
    stdio.println("KyneOS Logon Interface")
    shellPrefData: dict = process.getPreferenceOf("Local:me.lks410.kyneos.kyneui")
    if shellPrefData == {}:
        process.setPreferenceOf("Local:me.lks410.kyneos.kyneui", {
            "LineFormat": "{username}@{hostname}{domain}: {cwd} {privilege} ",
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

    while process.isRunning:
        cwd = process.cwd
        shellPrefData = process.getPreferenceOf("Local:me.lks410.kyneos.kyneui")
        formattedLine = shellPrefData["LineFormat"]
        formattedLine = formattedLine.replace("{username}", process.ownerUser.username)
        formattedLine = formattedLine.replace("{hostname}", hostData["machineName"])
        formattedLine = formattedLine.replace("{cwd}", cwd if cwd != process.ownerUser.home else "~")
        formattedLine = formattedLine.replace("{privilege}", "#" if process.ownerUser.isAdministrator() else "$")

        domain = process.ownerUser.email.split("@")[1]
        if domain != "localhost":
            formattedLine = formattedLine.replace("{domain}", f"({domain})")
        else:
            formattedLine = formattedLine.replace("{domain}", "")

        stdio.printf(formattedLine, end="")
        command = stdio.scanf()
        commandComponents: list = shell.splitStringBySpaceWhileConsideringEscapeAndQuotation(command)

        if len(commandComponents[0]) == 0:
            continue

        if command == "exit" or command == "logout":
            break
        else:
            shell.interpretParameters(commandComponents, process)

