import os
import shutil

import System.Library.Security.APIAccessControls as APIAccessControls

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "fs",
        "id": "kfs",
        "name": "KyneFS",
        "version": "1.0.0",
        "description": "Kyne File System Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0,
        "functions": [
            "reads(str):str",
            "writes(str,str):bool",
            "isFile(str):bool",
            "isDir(str):bool",
            "listDir(str):list",
            "makeDir(str):bool",
            "remove(str):bool",
            "copy(str,str):bool",
            "move(str,str):bool",
            "rename(str,str):bool",
        ]
    }

def reads(path: str) -> str:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    with open(path, 'r') as f:
        return f.read()

def writes(path: str, content: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    with open(path, 'w') as f:
        f.write(content)
    return True

def isFile(path: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    return os.path.isfile(path)

def isDir(path: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    return os.path.isdir(path)

def listDir(path: str) -> list:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    return os.listdir(path)

def makeDir(path: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    os.makedirs(path, exist_ok=True)
    return True

def remove(path: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    path = os.path.abspath(f"{os.getcwd()}/{path}")
    os.remove(path)
    return True

def copy(src: str, dest: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    src = os.path.abspath(f"{os.getcwd()}/{src}")
    dest = os.path.abspath(f"{os.getcwd()}/{dest}")
    shutil.copy(src, dest)
    return True

def move(src: str, dest: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    src = os.path.abspath(f"{os.getcwd()}/{src}")
    dest = os.path.abspath(f"{os.getcwd()}/{dest}")
    shutil.move(src, dest)
    return True

def rename(src: str, dest: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures.execspaces"):
        raise Exception("Access denied.")
    src = os.path.abspath(f"{os.getcwd()}/{src}")
    dest = os.path.abspath(f"{os.getcwd()}/{dest}")
    os.rename(src, dest)
    return True


