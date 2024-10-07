
def syscall(callID: str, func: str, args: any = None, kwargs: any = None) -> any:
    from System.Library.execspaces import KernelSpace
    return KernelSpace.syscall(callID, func, args, kwargs)

def invoke(callID: str, func: str, args: any) -> any:
    syscall(callID, func, args)
