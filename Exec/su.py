from System.Library.Objects.Process import Process
from System.Library.Objects.DSObject import DSObject
from System.Library.Objects.User import User

import System.stdio as stdio

def main(args, process: Process):
    if not process.ownerUser.isAdministrator():
        stdio.printf("Password >> ", end="")
        password = stdio.scanf()
        if process.ownerUser.escalatePrivilege(process.ownerUser.username, password):
            if process.ownerUser.isAdministrator():
                return 0
            else:
                stdio.println("Escalation failed.")
                return 1
        else:
            stdio.println("Escalation failed.")
            return 1
    else:
        process.ownerUser.restoreDefaultPrivilege()
        return 0

