from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

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
        self.username = dsObject.getAttribute("username")
        self.fullName = dsObject.getAttribute("name")
        self.displayName = dsObject.getAttribute("label")
        self.email = f"{self.username}@{dsObject.getDomain()}"
        self.home = dsObject.getAttribute("home")
        self.ui = dsObject.getAttribute("ui")
        self.shell = dsObject.getAttribute("shell")
