from System.Library.execspaces import KernelSpace

def run(frameworkPath: str, frameworkParameters: dict, process, doAsync: bool = False):
    return KernelSpace.syscall("ext.kyne.frameworksupport", "run", frameworkPath, frameworkParameters, process, doAsync)
