from System.Library.execspaces import KernelSpace

def run(frameworkPath: str, frameworkParameters: dict, process, doAsync: bool = False):
    return KernelSpace.syscall("ext.kyne.frameworksupport", "runFramework", frameworkPath, frameworkParameters, process, doAsync)
