from System.Library.CoreInfrastructures.Objects.Process import Process
from System.Library.CoreInfrastructures.Objects.DSObject import DSObject
from System.Library.CoreInfrastructures.Objects.User import User

import System.stdio as stdio

def main(args, process: Process):
    if not process.ownerUser.isAdministrator():
        stdio.printf("Password >> ", end="")
        password = stdio.scanf()
        if process.ownerUser.escalatePrivilege(process.ownerUser.username, password):
            stdio.println("Privilege escalated.")
        else:
            stdio.println("Escalation failed.")
    else:
        process.ownerUser.restoreDefaultPrivilege()
        stdio.println("Privilege restored.")

