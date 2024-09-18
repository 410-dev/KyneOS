from System.Library.CoreInfrastructures.Objects.Process import Process
from System.Library.CoreInfrastructures.Objects.DSObject import DSObject
from System.Library.CoreInfrastructures.Objects.User import User

import System.stdio as stdio

def main(args, process: Process):
    stdio.printf("Password >> ", end="")
    password = stdio.scanf()
    if process.ownerUser.escalatePrivilege(process.ownerUser.username, password):
        try:
            pass
            # DO SOMETHING
        except Exception as e:
            stdio.println(f"Error: {e}")
    else:
        stdio.println("Escalation failed.")
        return
    process.ownerUser.restoreDefaultPrivilege()
