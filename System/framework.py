from System.Library.execspaces import KernelSpace

def run(frameworkPath: str, frameworkParameters: dict, process, doAsync: bool = False):
    return KernelSpace.syscall("ext.kyne.frameworksupport", "runFramework", frameworkPath, frameworkParameters, process, doAsync)

def getFrameworkAttribute(frameworkPath, process):
    return KernelSpace.syscall("ext.kyne.frameworksupport", "getFrameworkAttribute", frameworkPath, process)

def getFrameworkResource(frameworkPath, process, resourceId):
    return KernelSpace.syscall("ext.kyne.frameworksupport", "getFrameworkResource", frameworkPath, process, resourceId)