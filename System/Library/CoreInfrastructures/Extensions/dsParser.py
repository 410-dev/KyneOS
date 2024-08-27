import json

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
    fs.writes(pathFull, json.dumps(objectData))
    return True

def createObjectExternalAttribute(path: str, key: str, value) -> bool:
    if not APIAccessControls.isAccessFromScope("System.Library.CoreInfrastructures"):
        raise Exception("Access denied.")

    if path.startswith("/"):
        path = path[1:]
    pathFull = f"/Library/DirectoryService/{path}/{key}.json"
    fs.writes(pathFull, json.dumps(value))
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
