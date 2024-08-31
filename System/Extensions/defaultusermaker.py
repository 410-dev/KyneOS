def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "setup",
        "id": "defaultusermaker",
        "name": "KyneOS Time Manager",
        "version": "1.0.0",
        "description": "KyneOS Time Manager Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }

from System.Library.CoreInfrastructures.execspaces import KernelSpace
from System.Library.CoreInfrastructures.Objects.User import User
import System.stdio as stdio
defaultUser = User(None, path="/Local/localhost/kyne")
if defaultUser.fullName is None:
    stdio.println("Creating default user 'kyne'...")
    KernelSpace.syscall("ext.kyne.authman", "createUser", "kyne", "kyne", "Local", "localhost", "", True)
