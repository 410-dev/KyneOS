import System.fs as fs
import System.stdio as stdio

def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "sys",
        "id": "bootlogodisplay",
        "name": "Boot Logo Display",
        "version": "1.0.0",
        "description": "Boot Logo Display Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }

stdio.println(fs.reads("/Library/etc/logo-asciix49.txt"))
