import importlib
import os
import sys
import time

import System.Library.Security.APIAccessControls as APIAccessControls


class KernelSpace:
    loaded: dict[str, dict] = {
        # "ext.fs.kfs": {
        #     "name": "KyneFS",
        #     "version": "1.0.0",
        #     "description": "Kyne File System Extension",
        #     "author": "LKS410",
        #     "license": "MIT",
        #     "file": "/System/Library/Drivers/kfs.py",
        #     "functions": [
        #         "reads(str):str",
        #         "write(str,str):bool",
        #     ],
        #     "exec": None  # Actual extension object
        # }
    }

    _kernelUser = None

    @staticmethod
    def syscall(ksObjId: str, functionName: str, *args, **kwargs):
        driverObj = KernelSpace.loaded.get(ksObjId)
        if not driverObj:
            raise Exception(f"Driver {ksObjId} is not loaded.")

        driverInstance = driverObj.get("exec")
        if not driverInstance:
            raise Exception(f"Driver {ksObjId} is loaded but not initialized or not runnable.")

        func = getattr(driverInstance, functionName)
        if not func:
            raise Exception(f"Function {functionName} not found in driver {ksObjId}.")

        return func(*args, **kwargs)

    @staticmethod
    def unregister(ksObjId: str):
        KernelSpace.loaded.pop(ksObjId)

    @staticmethod
    def startService(bundlePath: str, bootParameters: list, restartService: bool = False):
        from System.Library.CoreInfrastructures.Objects.Bundle import Bundle
        from System.Library.CoreInfrastructures.Objects.Process import Process

        bundle = Bundle(bundlePath)
        processObj = Process(bundle.displayName, bundle.getExecutable(), [], KernelSpace._kernelUser)
        processObj.launchAsync(bootParameters)

    @staticmethod
    def load(filePath: str, sysargs: list[str], isBundle: bool = True):
        from System.Library.CoreInfrastructures.Objects.Bundle import Bundle
        bundlePath: str = ""
        if isBundle:
            bundlePath = filePath
            filePath = f"{filePath}/main.py"
        modulePath = filePath.replace("/", ".").replace(".py", "").replace(os.path.sep, ".")
        if modulePath.startswith("."):
            modulePath = modulePath[1:]

        # if
        # module = importlib.import_module(modulePath)
        # importlib.reload(module)
        if modulePath in sys.modules:
            # module = importlib.import_module(modulePath)
            module = sys.modules[modulePath]
            importlib.reload(module)
        else:
            module = importlib.import_module(modulePath)

        requiredFields = [
            "type",
            "class",
            "id",
            "name",
            "version",
        ]

        if not isBundle:
            if not hasattr(module, "DECLARATION"):
                raise Exception("KernelSpace object must have a DECLARATION function that returns a dictionary.")

            ksObjData: dict = module.DECLARATION()
            for field in requiredFields:
                if not ksObjData.get(field):
                    if not isBundle:
                        raise Exception(f"Field {field} is required in DECLARATION function returned dictionary.")

            if hasattr(module, "INIT"):
                returned: int = module.INIT(sysargs)
                if returned != 0:
                    raise Exception(f"Failed initializing kernel object {ksObjData.get('name')}.")

        else:
            for i, field in enumerate(requiredFields):
                field = field[0].upper() + field[1:]
                requiredFields[i] = field
            bundle: Bundle = Bundle(bundlePath)
            ksObjData: dict = {}
            for field in requiredFields:
                if not bundle.getAttributeOf(field):
                    raise Exception(f"Field {field} is required in bundle attribute.")
                ksObjData[field.lower()] = bundle.getAttributeOf(field)

        ksObjId = f"{ksObjData.get('type')}.{ksObjData.get('class')}.{ksObjData.get('id')}"

        KernelSpace.loaded[ksObjId] = {
            "name": ksObjData.get("name"),
            "version": ksObjData.get("version"),
            "description": ksObjData.get("description") if ksObjData.get("description") else "",
            "author": ksObjData.get("author") if ksObjData.get("author") else "",
            "license": ksObjData.get("license") if ksObjData.get("license") else "",
            "file": filePath,
            "functions": ksObjData.get("functions") if ksObjData.get("functions") else [],
            "exec": module
        }

    @staticmethod
    def init():
        from System.Library.CoreInfrastructures.Objects.User import User
        from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

        if not KernelSpace._kernelUser:
            dso: DSObject = DSObject("/Local/localhost/KERNEL_USER")
            KernelSpace._kernelUser = User(dso)


from System.Library.CoreInfrastructures.Objects.User import User
class UserSpace:

    localLogon: dict[str, dict] = {
        
    }

    processes: dict[int, "Process"] = {

    }

    loaded: dict[str, dict] = {
        # "ext.fs.kfs": {
        #     "name": "KyneFS",
        #     "version": "1.0.0",
        #     "description": "Kyne File System Extension",
        #     "author": "LKS410",
        #     "license": "MIT",
        #     "file": "/System/Library/Drivers/kfs.py",
        # }
    }

    pid = 0
    _administratorUser = None

    @staticmethod
    def syscall(ksObjId: str, functionName: str, *args, **kwargs):
        driverObj = UserSpace.loaded.get(ksObjId)
        if not driverObj:
            raise Exception(f"Extension {ksObjId} is not loaded.")

        driverInstance = driverObj.get("exec")
        if not driverInstance:
            raise Exception(f"Extension {ksObjId} is loaded but not initialized or not runnable.")

        func = getattr(driverInstance, functionName)
        if not func:
            raise Exception(f"Extension {functionName} not found in extension file {ksObjId}.")

        return func(*args, **kwargs)

    @staticmethod
    def logon(user: User):
        UserSpace.localLogon[f"{user.email}:{user.home}"] = {
            "user": user,
            "logonTime": time.time(),
            "ownerProcess": None
        }

    @staticmethod
    def logoff(user: User):
        UserSpace.localLogon.pop(f"{user.email}:{user.home}")

    @staticmethod
    def registerProcess(process: "Process"):
        UserSpace.processes[process.pid] = process

    @staticmethod
    def nextPID():
        UserSpace.pid += 1
        return UserSpace.pid

    @staticmethod
    def startService(ownerUser: User, bundlePath: str, restartService: bool = False):
        UserSpace.openBundle(ownerUser, True, bundlePath, [])

    @staticmethod
    def openBundle(ownerUser: User, usingAsync: bool, bundlePath: str, args: list):
        from System.Library.CoreInfrastructures.Objects.Bundle import Bundle
        bundle = Bundle(bundlePath)
        return UserSpace.openExecutable(ownerUser, usingAsync, bundle.getExecutable(), args)

    @staticmethod
    def openExecutable(ownerUser: User, usingAsync: bool, executablePath: str, args: list) -> int:
        from System.Library.CoreInfrastructures.Objects.Process import Process
        processObj = Process(executablePath, executablePath, args, ownerUser)

        if usingAsync:
            return processObj.launchAsync(args)
        else:
            return processObj.launchSync(args)

    @staticmethod
    def init():
        from System.Library.CoreInfrastructures.Objects.User import User
        from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

        dso: DSObject = DSObject("/Local/localhost/Administrator")
        UserSpace._administratorUser = User(dso)

