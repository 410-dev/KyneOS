import asyncio

import System.stdio as stdio
from System.Library.CoreInfrastructures.Objects.DSObject import DSObject
from System.Library.CoreInfrastructures.Objects.Process import Process

from System.Library.CoreInfrastructures.Objects.User import User
from System.Library.CoreInfrastructures.execspaces import KernelSpace, UserSpace

doTerminate = False

async def mainAsync(args: list, process):
    # Switch TTY to 2
    process.assignedTTY = 2
    KernelSpace.syscall("drv.io.tty", "switchTTY", 2, True)

    stdio.println("KyneOS Logon Interface")

    while (not doTerminate) and process.isRunning:
        try:
            stdio.printf("Login: ", end="")
            username = stdio.scanf()
            if username == "exit":
                stdio.println("Killing initsys...")
                UserSpace.processes.get(1).kill(0)
                return
            stdio.printf("Password: ", end="")
            password = stdio.scanf()

            success, message, user = KernelSpace.syscall("ext.kyne.authman", "validateUser", username, password, "Local", "localhost", "")

            if not success:
                stdio.println(message)
                continue
            else:
                stdio.println(message)
                user: DSObject = user
                user: User = User(user)
                UserSpace.openBundle(user, False, f"/System/SystemUserInterfaces/{user.ui}", args)
        except Exception as e:
            stdio.println(f"Logon error: {e}")
            continue