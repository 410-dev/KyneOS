import os.path

from System.Library.CoreInfrastructures.execspaces import KernelSpace

class DSObject:

    TYPES = {
        "LocalObject": "LO",
        "Site": "ST",
        "DomainController": "DC",
        "OrganizationalUnit": "OU",
        "ForestRoot": "FR",
    }

    def __init__(self, path: str, objectData: dict = None):
        if path == "CurrentMachine":
            path = "/Local/localhost"
        self.path = path
        self.objectData = objectData
        if objectData is None:
            dobj: "DSObject" = KernelSpace.syscall("ext.directory.dsparser", "getObject", path)
            if dobj is None:
                raise FileNotFoundError(f"Object not found at path: {path}")
            self.objectData = dobj.objectData
        self.parentsObject = []
        lastObject: "DSObject" = self
        while lastObject.getType() != "FR":
            lastObject = lastObject.getParentObject()
            self.parentsObject.append(lastObject)
        self.parentsObject.reverse()

    @staticmethod
    def UserObjectData(username: str, fullName: str, displayName: str, location: str, description: str, authManHash: str, authManPK: str) -> dict:
        key = "LocalObject"
        return {
            "type": DSObject.TYPES[key],
            f"{DSObject.TYPES[key].lower()}.type": "User",
            # f"{DSObject.TYPES[key].lower()}.username": username,
            f"{DSObject.TYPES[key].lower()}.name": fullName,
            f"{DSObject.TYPES[key].lower()}.label": displayName,
            f"{DSObject.TYPES[key].lower()}.location": location,
            f"{DSObject.TYPES[key].lower()}.description": description,
            f"{DSObject.TYPES[key].lower()}.home": f"/Users/{username}",
            f"{DSObject.TYPES[key].lower()}.authorization": {
                "AuthManHash": authManHash,
                "AuthManPK": authManPK
            }
        }


    def getChildObject(self, path: str) -> "DSObject":
        return KernelSpace.syscall("ext.directory.dsparser", "getObject", f"{self.path}/{path}")

    def getParentObject(self, objectType: str = None) -> "DSObject":
        if objectType:
            for parent in self.parentsObject:
                if parent.getType() == objectType:
                    return parent
        return KernelSpace.syscall("ext.directory.dsparser", "getObject", os.path.dirname(self.path))

    def getAttribute(self, key: str):
        if key in self.objectData:
            return self.objectData[key]
        elif f"{self.getType().lower()}.{key}" in self.objectData:
            return self.objectData[f"{self.getType().lower()}.{key}"]
        else:
            return None

    def getType(self):
        return self.objectData["type"]

    def createObject(self, path: str, objectData: dict):
        KernelSpace.syscall("ext.directory.dsparser", "createObject", f"{self.path}/{path}", objectData)

    def setAttribute(self, key: str, value):
        self.objectData[key] = value

    def getExternalAttribute(self, key: str):
        return KernelSpace.syscall("ext.directory.dsparser", "getObjectExternalAttribute", self.path, key)

    def save(self):
        KernelSpace.syscall("ext.directory.dsparser", "createObject", self.path, self.objectData)

    def getName(self):
        return os.path.basename(self.path)

    def getDomain(self):
        for parent in self.parentsObject:
            if parent.getType() == "DC":
                return parent.getName()

    def getPolicy(self) -> dict:
        policy = {}
        priorityLowToHigh = ["LO", "ST", "DC", "OU"]
        for objType in priorityLowToHigh:
            for parent in self.parentsObject:
                if parent.getType() == objType:
                    policy.update(parent.getExternalAttribute("policy"))
        return policy

    def getPolicyValue(self, key: str, default):
        policy = self.getPolicy()
        if key in policy:
            return policy[key]
        else:
            return default

    def __str__(self):
        return f"DSObject(TYPE={self.getType()},NAME={self.getName()},PATH={self.path},DOM={self.getDomain()})"

