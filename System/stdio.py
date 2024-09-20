from System.Library.execspaces import KernelSpace

def printf(string: any, end: str = "", tty: int = -1):
    KernelSpace.syscall("drv.io.stdout", "println", f"{string}", end=end, tty=tty)

def println(string: any, tty: int = -1):
    KernelSpace.syscall("drv.io.stdout", "println", f"{string}", tty=tty)

def scanf() -> str:
    return KernelSpace.syscall("drv.io.stdin", "scan")