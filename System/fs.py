from System.Library.CoreInfrastructures.execspaces import KernelSpace

def reads(path: str) -> str:
    return KernelSpace.syscall("ext.fs.kfs", "reads", path)

def writes(path: str, data: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "writes", path, data)

def isFile(path: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "isFile", path)

def isDir(path: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "isDir", path)

def listDir(path: str) -> list:
    return KernelSpace.syscall("ext.fs.kfs", "listDir", path)

def makeDir(path: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "makeDir", path)

def remove(path: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "remove", path)

def copy(src: str, dest: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "copy", src, dest)

def move(src: str, dest: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "move", src, dest)

def rename(src: str, dest: str) -> bool:
    return KernelSpace.syscall("ext.fs.kfs", "rename", src, dest)

def exists(path: str) -> bool:
    return isFile(path) or isDir(path)
