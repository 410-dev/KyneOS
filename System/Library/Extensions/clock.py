from datetime import datetime

import System.Library.Security.APIAccessControls as APIAccessControls

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "time",
        "id": "clock",
        "name": "KyneOS Time Manager",
        "version": "1.0.0",
        "description": "KyneOS Time Manager Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }


startupTime: int = round(datetime.now().timestamp())


def getStartupTime() -> int:
    return startupTime
