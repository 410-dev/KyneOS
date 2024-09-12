from System.Library.CoreInfrastructures.execspaces import KernelSpace

def DECLARATION() -> dict:
    return {
        "type": "drv",
        "class": "hw",
        "id": "nvram",
        "name": "vNVRAM",
        "version": "1.0.0",
        "description": "NVRAM Virtualization & Abstraction Driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

def read(key: str) -> str:
    return KernelSpace.syscall("ext.hw.virtrw", "read", "nvram", key)

def write(key: str, value: str) -> bool:
    return KernelSpace.syscall("ext.hw.virtrw", "write", "nvram", value, key)

def remove(key: str) -> bool:
    return KernelSpace.syscall("ext.hw.virtrw", "remove", "nvram", key)
