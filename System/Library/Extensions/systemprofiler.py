import System.Library.kynekernel as kernelfile

def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "sys",
        "id": "profile",
        "name": "System Profiler",
        "version": "1.0.0",
        "description": "System Profiler Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

def getSystemProfile():
    return {
        "system": {
            "name": "KyneOS",
            "version": "1.0",
            "build": 1,
            "release": "alpha1",
            "distro": kernelfile.CURRENT_SYS_DISTRO
        },
        "kernel": {
            "name": kernelfile.CURRENT_KRNL_NAME,
            "version": kernelfile.CURRENT_KRNL_VERSION,
            "release": kernelfile.CURRENT_KRNL_TESTVRS
        }
    }