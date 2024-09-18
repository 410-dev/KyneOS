import os

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "vhardware",
        "id": "stddisplay",
        "name": "Standard Display Extension",
        "version": "1.0.0",
        "description": "Standard Display Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0,
    }


def clear():
    os.system('cls' if os.name=='nt' else 'clear')
