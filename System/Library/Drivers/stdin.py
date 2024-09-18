def DECLARATION() -> dict:
    return {
        "type": "drv",  # 3 letter type: ext, drv, svc
        "class": "io",
        "id": "stdin",
        "name": "Standard Input Driver",
        "version": "1.0.0",
        "description": "Standard Input Driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0,
        "functions": [
            "scan():str"
        ]
    }

def scan() -> str:
    return input()
