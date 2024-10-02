import System.stdio as stdio
import System.shexec as shexec

from System.Library.execspaces import KernelSpace

def main(args: list[str], process):
    if not KernelSpace.getCurrentDistro() == "Server":
        stdio.println("This command is only available on KyneOS Server.")
        return 1

    if not process.ownerUser.isAdministrator():
        stdio.println("This command requires administrative privileges.")
        return 1

    if len(args) < 2:
        stdio.println("Usage: server <command for server>")
        return 1

    additionalPaths: list[str] = [
        "/System/Server/Applications",
        "/System/Server/Exec",
        "/Library/Server/Applications",
        "/Library/Server/Exec"
    ]

    process.ownerUser.addTemporaryPaths(additionalPaths)

    args.pop(0)

    return shexec.interpretParameters(args, process)
