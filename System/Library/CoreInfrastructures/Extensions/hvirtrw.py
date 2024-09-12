import hashlib
import System.rawfs as fs

def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "hw",
        "id": "virtrw",
        "name": "Writable Hardware Emulator",
        "version": "1.0.0",
        "description": "Writable hardware emulator",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

def read(device: str, chunkId: str = "0") -> str:
    try:
        devicecode = hashlib.md5(device.encode()).hexdigest()
        chunkIdcode = hashlib.md5(f"{device}/{chunkId}".encode()).hexdigest()
        return fs.readb(f"/Library/HWAbstraction/{devicecode}-{chunkIdcode}").decode()
    except:
        return ""

def write(device: str, value: str, chunkId: str = "0") -> bool:
    try:
        fs.makeDir(f"/Library/HWAbstraction/")
        devicecode = hashlib.md5(device.encode()).hexdigest()
        chunkIdcode = hashlib.md5(f"{device}/{chunkId}".encode()).hexdigest()
        binaryData = bytes(value, 'utf-8')
        fs.writeb(f"/Library/HWAbstraction/{devicecode}-{chunkIdcode}", binaryData)
        return True
    except:
        return False

def remove(device: str, chunkId: str = "0") -> bool:
    try:
        devicecode = hashlib.md5(device.encode()).hexdigest()
        chunkIdcode = hashlib.md5(f"{device}/{chunkId}".encode()).hexdigest()
        fs.remove(f"/Library/HWAbstraction/{devicecode}-{chunkIdcode}")
        return True
    except:
        return False
