from System.Library.Objects.Process import Process

import System.stdio as stdio
import System.shexec as shell

def main(args, process: Process):
    stdio.printf("Password >> ", end="")
    password = stdio.scanf()
    args.pop(0)
    if process.ownerUser.escalatePrivilege(process.ownerUser.username, password):
        try:
            exitCode = shell.interpretLine(" ".join(args), process)
            process.ownerUser.restoreDefaultPrivilege()
            return exitCode
        except Exception as e:
            stdio.println(f"Error: {e}")
    else:
        stdio.println("Escalation failed.")
        return
    process.ownerUser.restoreDefaultPrivilege()
