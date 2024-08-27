import asyncio

import System.stdio as stdio

from System.Library.CoreInfrastructures.execspaces import KernelSpace

doTerminate = False

async def mainAsync(args: list, process):
    # Switch TTY to 2
    process.assignedTTY = 2
    KernelSpace.syscall("drv.io.tty", "switchTTY", 2)

    # Wait for 3 seconds
    await asyncio.sleep(3)

    stdio.println("KyneOS User Interface")

    while not doTerminate:
        stdio.printf("Login: ", end="")
        username = stdio.scanf()
        stdio.printf("Password: ", end="")
        password = stdio.scanf()

        success, message, user = KernelSpace.syscall("ext.kyne.authman", "validateUser", username, password, "Local", "localhost", "")

        if not success:
            stdio.println(message)
            continue
        else:
            stdio.println(message)
            break
