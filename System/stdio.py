from System.Library.CoreInfrastructures.execspaces import KernelSpace

def printf(string: str, end: str = "", tty: int = -1):
    KernelSpace.syscall("drv.io.stdout", "println", string, end=end, tty=tty)

def println(string: str, tty: int = -1):
    KernelSpace.syscall("drv.io.stdout", "println", string, tty=tty)

def scanf() -> str:
    return KernelSpace.syscall("drv.io.stdin", "scan")