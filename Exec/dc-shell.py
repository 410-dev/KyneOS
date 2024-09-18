from System.Library.Objects.Process import Process
from System.Library.Objects.DSObject import DSObject
from System.Library.Objects.User import User
from System.Library.execspaces import KernelSpace

import System.stdio as stdio
import System.fs as fs

inputQueue: list[str] = []

def nextInput(question: str = "") -> str:
    if question != "":
        stdio.printf(question, end="")
    if len(inputQueue) == 0:
        return stdio.scanf()
    data = inputQueue.pop(0)
    stdio.println(data)
    return data

def main(args, currentProcess: Process):
    if not currentProcess.ownerUser.isAdministrator():
        stdio.println("You must be an administrator to run this command.")
        return

    currentPosition = "/Local/localhost"
    rootPosition = "/Local/localhost"
    if KernelSpace.getCurrentDistro() == "Server":
        stdio.println("Server distro detected.")
        currentPosition = ""
        rootPosition = currentPosition

    currentObject = DSObject(currentPosition)

    commandsQueue = []
    stringBuild: str = ""
    args.pop(0)
    global inputQueue
    for arg in args:
        if arg == "++":
            commandsQueue.append(stringBuild.strip())
            stringBuild = ""
        else:
            stringBuild += arg + " "

    if stringBuild != "" or len(commandsQueue) != 0:
        commandsQueue.append(stringBuild.strip())
        commandsQueue.append("exit")

    inputQueue = commandsQueue

    while currentProcess.isRunning or len(commandsQueue) > 0:
        stdio.printf(f"{currentPosition} >> ", end="")
        command = nextInput()

        if command == "exit":
            break

        if command == "help":
            stdio.println("Available commands:")
            stdio.println("./<path>    - Change current directory")
            stdio.println("ls          - List directory contents")
            stdio.println("forest      - Create a forest")
            stdio.println("domain      - Create a domain")
            stdio.println("ou          - Create a organizational unit")
            stdio.println("site        - Manage a site")
            stdio.println("user        - Create a user")
            stdio.println("this        - Display current object information")
            stdio.println("exit - Exit the shell")
            stdio.println("help - Display this help message")
            stdio.println("")
            stdio.println("You can use one-line command by separating each command with ' ++ '")
            stdio.println("Example: ./Local ++ ls ++ exit")
            continue

        if command == "ls":
            try:
                if currentObject.getType() == DSObject.TYPES["LocalObject"]:
                    stdio.println("Local object cannot have children.")
                    continue
                dirList = fs.listDir(f"/Library/DirectoryService/{currentPosition}")
                for item in dirList:
                    if fs.isDir(f"/Library/DirectoryService/{currentPosition}/{item}"):
                        stdio.println(f"{item}")
            except Exception:
                stdio.println("List directory failed.")
                continue

        if command == "this":
            stdio.println(f"Name: {currentObject.getName()}")
            stdio.println(f"Type: {currentObject.getType()}")
            stdio.println(f"Domain: {currentObject.getDomain()}")
            attributes = currentObject.__dict__["objectData"]
            stdio.println("Attributes:")
            for key in attributes:
                stdio.println(f"    {key}: {attributes[key]}")
            continue

        if command.startswith("."):
            if command == "..":
                nextPosition = currentPosition.split("/")
                nextPosition.pop()
                nextPosition = "/".join(nextPosition)
                if len(nextPosition) < len(rootPosition):
                    stdio.println("Cannot go beyond root.")
                    continue
            elif command.startswith("./"):
                if currentObject.getType() == DSObject.TYPES["LocalObject"]:
                    stdio.println("Cannot go deeper than local object.")
                    continue
                nextPosition = f"{currentPosition}/{command[2:]}"
            else:
                if currentObject.getType() == DSObject.TYPES["LocalObject"]:
                    stdio.println("Cannot go deeper than local object.")
                    continue
                nextPosition = f"{currentPosition}/{command[1:]}"

            try:
                if not DSObject(nextPosition).exists():
                    stdio.println("Directory not found.")
                    continue
                currentPosition = nextPosition
                currentObject = DSObject(currentPosition)
            except Exception:
                stdio.println("Change directory failed.")
                continue

        commandComponents = command.split(" ")

        if commandComponents[0] == "forest":
            forestManagement(currentObject, commandComponents)

        elif commandComponents[0] == "domain":
            domainManagement(currentObject, commandComponents)

        elif commandComponents[0] == "ou":
            ouManagement(currentObject, commandComponents)

        elif commandComponents[0] == "site":
            siteManagement(currentObject, commandComponents)

        elif commandComponents[0] == "user":
            userManagement(currentObject, commandComponents)

    return 0


def forestManagement(currentObject: DSObject, commandComponents: list[str]):
    if KernelSpace.getCurrentDistro() != "Server":
        stdio.println("Forest management is only available on Server distro.")
        return

    if len(commandComponents) < 2:
        stdio.println("Usage: forest <create | delete>")
        return

    elif commandComponents[1] == "create":
        if len(commandComponents) < 3:
            stdio.println("Usage: forest create <name>")
            return

        forestName = commandComponents[2]
        try:
            if DSObject(f"/{forestName}").exists():
                stdio.println("Forest already exists.")
                return
        except Exception:
            pass

        forest = DSObject(f"/{forestName}")
        forest.createObject(forestName, {"name": forestName, "type": "Forest"})
        stdio.println("Forest created.")
    elif commandComponents[1] == "delete":
        if len(commandComponents) < 3:
            stdio.println("Usage: forest delete <name>")
            return
        forestName = commandComponents[2]
        forest = DSObject(f"/{forestName}")
        if not forest.exists():
            stdio.println("Forest not found.")
            return
        forest.deleteObject()
        stdio.println("Forest deleted.")
    else:
        stdio.println("Invalid command.")


def domainManagement(currentObject: DSObject, commandComponents: list[str]):
    if KernelSpace.getCurrentDistro() != "Server":
        stdio.println("Domain management is only available on Server distro.")
        return
    if len(commandComponents) < 2:
        stdio.println("Usage: domain <command>")
        stdio.println("Commands:")
        stdio.println("    create <name> - Create a domain")
        stdio.println("    delete - Delete the current domain")
        return

    elif commandComponents[1] == "create":
        if len(commandComponents) < 3:
            stdio.println("Usage: domain create <name>")
            return
        domainName = commandComponents[2]
        forest = currentObject.getParentObject(objectType=DSObject.TYPES["ForestRoot"])
        forest.createObject(f"{domainName}", {"type": DSObject.TYPES["DomainController"], "dc.usernames": []})
        stdio.println("Domain created.")

    elif commandComponents[1] == "delete":
        if len(commandComponents) < 2:
            stdio.println("Usage: domain delete")
            stdio.println("This will delete the current domain.")
            return

        domain: DSObject
        if currentObject.getType() == DSObject.TYPES["DomainController"]:
            domain = currentObject
        else:
            domain = currentObject.getParentObject(objectType=DSObject.TYPES["DomainController"])

        if not domain.exists():
            stdio.println("Domain not found.")

        domain.deleteObject()
        stdio.println("Domain deleted.")
    else:
        stdio.println("Invalid command.")


def ouManagement(currentObject: DSObject, commandComponents: list[str]):
    if KernelSpace.getCurrentDistro() != "Server":
        stdio.println("Organizational unit management is only available on Server distro.")
        return

    if len(commandComponents) < 2:
        stdio.println("Usage: ou <command>")
        stdio.println("Commands:")
        stdio.println("    create <name> - Create an organizational unit")
        stdio.println("    delete - Delete the current organizational unit")
        # stdio.println("    list - List organizational units")
        return

    if commandComponents[1] == "create":
        if len(commandComponents) < 3:
            stdio.println("Usage: ou create <name>")
            return
        ouName = commandComponents[2]
        currentObject.createObject(f"{ouName}", {"type": DSObject.TYPES["OrganizationalUnit"]})
        stdio.println("Organizational unit created.")
    elif commandComponents[1] == "delete":
        if len(commandComponents) < 2:
            stdio.println("Usage: ou delete")
            stdio.println("This will delete the current organizational unit.")
            return
        if not currentObject.exists():
            stdio.println("Organizational unit not found.")
            return
        currentObject.deleteObject()
        stdio.println("Organizational unit deleted.")
    else:
        stdio.println("Invalid command.")

    return

def siteManagement(currentObject: DSObject, commandComponents: list[str]):
    if KernelSpace.getCurrentDistro() != "Server":
        stdio.println("Site management is only available on Server distro.")
        return

    if len(commandComponents) < 2:
        stdio.println("Usage: site <command>")
        stdio.println("Commands:")
        stdio.println("    create <name> - Create a site")
        stdio.println("    delete - Delete the current site")
        return

    if commandComponents[1] == "create":
        if len(commandComponents) < 3:
            stdio.println("Usage: site create <name>")
            return
        siteName = commandComponents[2]
        currentObject.createObject(f"{siteName}", {"type": DSObject.TYPES["Site"]})
        stdio.println("Site created.")
    elif commandComponents[1] == "delete":
        if len(commandComponents) < 2:
            stdio.println("Usage: site delete")
            stdio.println("This will delete the current site.")
            return
        if not currentObject.exists():
            stdio.println("Site not found.")
            return
        currentObject.deleteObject()
        stdio.println("Site deleted.")
    else:
        stdio.println("Invalid command.")

    return

def userManagement(currentObject: DSObject, commandComponents: list[str]):
    if len(commandComponents) < 2:
        stdio.println("Usage: user <command>")
        stdio.println("Commands:")
        stdio.println("    create <username> - Create a user")
        stdio.println("    delete - Delete the current user")
        stdio.println("    inspect - Display user information")
        stdio.println("    modify - Modify user information")
        return

    if commandComponents[1] == "create":
        if len(commandComponents) < 3:
            stdio.println("Usage: user create <username>")
            return
        username = commandComponents[2]
        if currentObject.getChildObject(username) is not None:
            stdio.println("User already exists.")
            return
        password = nextInput("Password: ")
        passwordConfirm = nextInput("Confirm password: ")
        if password != passwordConfirm:
            stdio.println("Passwords do not match.")
            return
        from System.Library.execspaces import KernelSpace
        dc = currentObject.getDomain()
        fr = currentObject.getForest()
        route = currentObject.getLocalPath()
        stdio.println(f"Creating default user '/{fr}/{dc}/{route}/{username}'...")
        KernelSpace.syscall("ext.kyne.authman", "createUser", username, password, fr, dc, route, True)
        stdio.println("User created.")

