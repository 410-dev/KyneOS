from System.Library.CoreInfrastructures.execspaces import KernelSpace

def printf(string: str, end: str = ""):
    KernelSpace.syscall("drv.io.stdout", "println", string, end=end)

def println(string: str):
    KernelSpace.syscall("drv.io.stdout", "println", string)
