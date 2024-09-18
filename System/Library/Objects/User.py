import json

import System.fs as fs
from System.Library.Objects.DSObject import DSObject
from System.Library.execspaces import KernelSpace


class User:
    def __init__(self, dsObject: DSObject|None, path: str = None):
        if dsObject is None and path is None:
            raise ValueError("Either dsObject or path must be provided")
        if path is not None:
            try:
                dsObject = DSObject(path)
            except Exception:
                dsObject = DSObject(path, DSObject.UserObjectData(None, None, None, None, None, "", ""))
        self.dsObject = dsObject
        self.username = dsObject.getName()
        self.fullName = dsObject.getAttribute("name")
        self.displayName = dsObject.getAttribute("label")
        self.email = f"{self.username}@{dsObject.getDomain()}"
        self.home = dsObject.getAttribute("home")
        self.ui = dsObject.getAttribute("ui")
        self.shell = dsObject.getAttribute("shell")
        self.permission = 0

    def isAdministrator(self):
        return self.permission >= 32767

    def escalatePrivilege(self, adminName: str, adminPass: str, forest: str = "Local", domain: str = "localhost", directoryRoute: str = "/"):
        success, message, user = KernelSpace.syscall("ext.kyne.authman", "validateUser", adminName, adminPass, forest, domain, directoryRoute)
        if not success:
            return False, message

        user: DSObject = user
        maxPermission = user.getAttribute("authorization")["MaxPermission"]
        if maxPermission < 32767:
            return False, "Insufficient permissions."

        self.permission = maxPermission
        return True, "Authorization successful."

    def restoreDefaultPrivilege(self):
        self.permission = self.dsObject.getAttribute("authorization")["DefaultPermission"]


    def createHomeDirectory(self):
        requiredDirStruct: list = [
            "/Library/Preferences",
            "/Library/Extensions",
            "/Library/Services",
            "/Library/Drivers",
            "/Library/Events",
        ]

        for directory in requiredDirStruct:
            fs.makeDir(f"{self.home}{directory}")

    def getExecPaths(self):
        paths: list[str] = []

        globalPathEnforcement: list = self.dsObject.getPolicyValue("SystemAdministration.Exec.EnforcedPaths", [])
        enforceEnforcedOnly: bool = self.dsObject.getPolicyValue("SystemAdministration.Exec.EnforceEnforcedOnly", False)
        globalPathDefaults: list = self.dsObject.getPolicyValue("SystemAdministration.Exec.DefaultPaths", [])
        allowUserEditPath: bool = self.dsObject.getPolicyValue("UserAdministration.Exec.AllowUserEditPath", True)

        if globalPathEnforcement:
            paths.extend(globalPathEnforcement)
            if enforceEnforcedOnly:
                return paths
        if globalPathDefaults:
            paths.extend(globalPathDefaults)

        if allowUserEditPath:
            if fs.exists(f"{self.home}/Library/Preferences/me.lks410.kyneos.kyneui.json"):
                userPaths = json.loads(fs.reads(f"{self.home}/Library/Preferences/me.lks410.kyneos.kyneui.json")).get("PATH", [])
                paths.extend(userPaths)
            from System.Library.execspaces import UserSpace
            envPath = UserSpace.env(self.email, "PATH")
            if envPath:
                paths.extend(envPath.split(":"))

        return paths

    def __str__(self):
        return f"User: {self.username} ({self.fullName})"