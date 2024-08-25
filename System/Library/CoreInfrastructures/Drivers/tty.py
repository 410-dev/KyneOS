def DECLARATION() -> dict:
    return {
        "type": "drv",
        "class": "io",
        "id": "tty",
        "name": "tty",
        "version": "1.0.0",
        "description": "Multiple display TTY driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 999
    }

currentDisplayTTY = 0
displayTTYs = []
