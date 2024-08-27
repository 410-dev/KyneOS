def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "struct",
        "id": "directories",
        "name": "KyneOS Directory builder",
        "version": "1.0.0",
        "description": "Builds necessary directories for KyneOS",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }

import System.fs as fs
fs.makeDir("/tmp")
