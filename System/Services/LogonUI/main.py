import asyncio
import time

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
            currentMachine = DSObject("/Local/localhost")
            autoLogon = KernelSpace.syscall("ext.kyne.authman", "autoLogonEnabled")
            if not autoLogon:
                stdio.printf("Login: ", end="")
                username = stdio.scanf()
                if username == "exit":
                    stdio.println("Killing initsys...")
                    for pid, p in UserSpace.processes.items():
                        if p.executable == "/System/Library/initsys.py":
                            stdio.println(f"Found initsys at PID {pid}")
                            p.kill(0)
                            break
                    # UserSpace.processes.get(1).kill(0)
                    return
                stdio.printf("Password: ", end="")
                password = stdio.scanf()

                if username == "" or password == "":
                    continue

                success, message, user = KernelSpace.syscall("ext.kyne.authman", "validateUser", username, password, "Local", "localhost", "")

            else:
                success, message, user = KernelSpace.syscall("ext.kyne.authman", "autoLogon", "Local", "localhost", "")

            if not success:
                stdio.println("Logon error: " + message)
                time.sleep(currentMachine.getPolicyValue("SystemAdministration.Security.InteractiveLogon.TimeoutPerFailedAttempt", 1))
                continue
            else:
                user: DSObject = user
                user: User = User(user)
                UserSpace.openBundle(user, False, f"/System/SystemUserInterfaces/{user.ui}", args, user.home)

        except Exception as e:
            stdio.println(f"Logon error: {e}")
            continue