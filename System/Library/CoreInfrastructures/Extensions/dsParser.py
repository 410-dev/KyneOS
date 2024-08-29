import json
import os.path

import System.Library.Security.APIAccessControls as APIAccessControls
import System.fs as fs

from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "directory",
        "id": "dsparser",
        "name": "KyneOS Directory Service Parser",
        "version": "1.0.0",
        "description": "KyneOS Directory Service Parser Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

def getObject(path: str) -> DSObject | None:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathFull = f"/Library/DirectoryService/{path}/object.json"
    if fs.isFile(pathFull):
        objectData = fs.reads(pathFull)
        return DSObject(path, json.loads(objectData))
    else:
        return None

def getObjectExternalAttribute(path: str, key: str) -> dict:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathFull = f"/Library/DirectoryService/{path}/{key}.json"
    if fs.isFile(path):
        objectData = fs.reads(pathFull)
        return json.loads(objectData)
    else:
        return {}

def createObject(path: str, objectData: dict) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathFull = f"/Library/DirectoryService/{path}/object.json"

    if not fs.isDir(f"/Library/DirectoryService/{path}"):
        if not fs.isDir(f"/Library/DirectoryService/{os.path.dirname(path)}"):
            raise FileNotFoundError(f"Directory not found: {os.path.dirname(path)}")
        else:
            fs.makeDir(f"/Library/DirectoryService/{path}")

    fs.writes(pathFull, json.dumps(objectData, indent=4))

    if objectData.get("type") == "LO" and objectData.get("lo.type") == "User":
        dsObj = DSObject(path, objectData)
        dc: DSObject = dsObj.getParentObject("DC")
        while "//" in path:
            path = path.replace("//", "/")
        email: str = f"{dsObj.getName()}@{dsObj.getDomain()}"
        strValue: str = f"{email}:/{path}"
        replaced: bool = False
        for idx, user in enumerate(dc.getAttribute("dc.usernames")):
            if f"{email}:" in user:
                dc.getAttribute("dc.usernames")[idx] = strValue
                replaced = True
                break
        if not replaced:
            dc.getAttribute("dc.usernames").append(strValue)
        dc.save()

    return True


def deleteObject(path: str) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathDir = f"/Library/DirectoryService/{path}"
    pathFull = f"{pathDir}/object.json"

    if not fs.isFile(pathFull):
        raise FileNotFoundError(f"File not found: {pathFull}")

    dso: DSObject = DSObject(path)
    if dso.getType() == "LO" and dso.getAttribute("lo.type") == "User":
        dc: DSObject = dso.getParentObject("DC")
        email: str = f"{dso.getName()}@{dso.getDomain()}"
        for idx, user in enumerate(dc.getAttribute("dc.usernames")):
            if f"{email}:" in user:
                dc.getAttribute("dc.usernames").pop(idx)
                break
        dc.save()
    fs.remove(pathDir)
    return True


def createObjectExternalAttribute(path: str, key: str, value) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathFull = f"/Library/DirectoryService/{path}/{key}.json"
    fs.writes(pathFull, json.dumps(value, indent=4))
    return True

def enumerateChildren(path: str) -> dict:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]

    pathFull = f"/Library/DirectoryService/{path}"

    if not fs.isDir(pathFull):
        raise FileNotFoundError(f"Directory not found: {pathFull}")

    children = fs.listDir(pathFull)
    childrenDataWithTypes = {}
    for child in children:
        childPath = f"{pathFull}/{child}"
        if fs.isDir(childPath) and fs.isFile(f"{childPath}/object.json"):
            childrenDataWithTypes[child] = "object"
        elif childPath.endswith(".json") and childPath != f"{pathFull}/object.json":
            childrenDataWithTypes[child] = "attribute"
    return childrenDataWithTypes
