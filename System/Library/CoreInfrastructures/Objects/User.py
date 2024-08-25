from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

class User:

    def __init(self, dsObject: DSObject):
        self.dsObject = dsObject
        self.username = dsObject.getAttribute("username")
        self.fullName = dsObject.getAttribute("name")
        self.displayName = dsObject.getAttribute("label")
        self.email = f"{self.username}@{dsObject.getDomain()}"
        self.home = dsObject.getAttribute("home")
