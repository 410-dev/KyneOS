def DECLARATION() -> dict:
    return {
        "type": "drv",  # 3 letter type: ext, drv, svc
        "class": "io",
        "id": "stdout",
        "name": "Standard Output Driver",
        "version": "1.0.0",
        "description": "Standard Output Driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0,
        "functions": [
            "println(str,str):None",
        ]
    }

def println(content: str, end: str = "\n", tty: int = -1):
    print(content, end=end)
