
def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "kyne",
        "id": "frameworksupport",
        "name": "KyneOS System Framework Support",
        "version": "1.0.0",
        "description": "Memory support for KyneOS system frameworks",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }


class FRAMEWORK_MEMORY:
    mem = dict[str, dict[str, any]]()

def getMemoryValue(frameworkId: str, key: str) -> any:
    if frameworkId in FRAMEWORK_MEMORY.mem:
        if key in FRAMEWORK_MEMORY.mem[frameworkId]:
            return FRAMEWORK_MEMORY.mem[frameworkId][key]
    return None

def setMemoryValue(frameworkId: str, key: str, value: any) -> None:
    if frameworkId not in FRAMEWORK_MEMORY.mem:
        FRAMEWORK_MEMORY.mem[frameworkId] = dict[str, any]()
    FRAMEWORK_MEMORY.mem[frameworkId][key] = value

def removeMemoryValue(frameworkId: str, key: str) -> None:
    if frameworkId in FRAMEWORK_MEMORY.mem:
        if key in FRAMEWORK_MEMORY.mem[frameworkId]:
            del FRAMEWORK_MEMORY.mem[frameworkId][key]


def runFramework(frameworkPath: str, frameworkParameters: dict, parentProcess, doAsync: bool = False) -> any:
    from System.Library.Objects.Process import Process
    import System.fs as fs

    # check if the bundle has framework executable
    if not fs.isFile(f"{frameworkPath}/framework.py"):
        raise Exception("Framework executable not found")
    else:
        frameworkPath = f"{frameworkPath}/framework.py"

    frameworkProcess = Process(frameworkPath, frameworkPath, [], parentProcess.ownerUser, parentProcess)

    if doAsync:
        frameworkProcess.launchAsync(frameworkParameters)
    else:
        return frameworkProcess.launchSync(frameworkParameters)

