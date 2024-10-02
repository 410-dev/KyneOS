import System.stdio as stdio
import System.shexec as shexec
import System.fs as fs

def main(args: list[str], process):

    while process.isRunning:
        stdio.println("KyneOS Server Control Interface")
        stdio.println("===============================")
        stdio.println("0. Exit")
        stdio.println("1. Package Manager")
        stdio.println("2. Services Running")
        stdio.printf(">> ", end="")
        userIn: str = stdio.scanf()

        if userIn == "0":
            return 0

        elif userIn == "1":
            fs.makeDir("/Library/etc/Server/packages")
            fs.makeDir("/Library/etc/Server/instances")
            shexec.interpretParameters(["/System/Server/Applications/ctl/support/package-manager", "/System/Server/Applications/ctl/support/packages.json"], process)

        elif userIn == "2":
            stdio.println("Sorry, the option is not ready yet.")

