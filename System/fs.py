from System.Library.execspaces import KernelSpace

FILESYS = "ext.fs.kfs"

def reads(path: str) -> str:
    return KernelSpace.syscall(FILESYS, "reads", path)

def readb(path: str) -> bytes:
    return KernelSpace.syscall(FILESYS, "readb", path)

def writes(path: str, data: str) -> bool:
    return KernelSpace.syscall(FILESYS, "writes", path, data)

def writeb(path: str, data: bytes) -> bool:
    return KernelSpace.syscall(FILESYS, "writeb", path, data)

def appends(path: str, data: str) -> bool:
    return KernelSpace.syscall(FILESYS, "appends", path, data)

def isFile(path: str) -> bool:
    return KernelSpace.syscall(FILESYS, "isFile", path)

def isDir(path: str) -> bool:
    return KernelSpace.syscall(FILESYS, "isDir", path)

def listDir(path: str) -> list:
    return KernelSpace.syscall(FILESYS, "listDir", path)

def makeDir(path: str) -> bool:
    return KernelSpace.syscall(FILESYS, "makeDir", path)

def remove(path: str) -> bool:
    return KernelSpace.syscall(FILESYS, "remove", path)

def copy(src: str, dest: str) -> bool:
    return KernelSpace.syscall(FILESYS, "copy", src, dest)

def move(src: str, dest: str) -> bool:
    return KernelSpace.syscall(FILESYS, "move", src, dest)

def rename(src: str, dest: str) -> bool:
    return KernelSpace.syscall(FILESYS, "rename", src, dest)

def exists(path: str) -> bool:
    return isFile(path) or isDir(path)

def accessible(path: str, mode: str, process) -> bool:
    return KernelSpace.syscall(FILESYS, "accessible", path, mode, process)
