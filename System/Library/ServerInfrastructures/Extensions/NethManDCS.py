import System.stdio as stdio
from System.Library.execspaces import KernelSpace

def DECLARATION() -> dict:
    return {
        "type": "ext",  # 3 letter type: ext, drv, svc
        "class": "serverinfra",
        "id": "nethmandcs",
        "name": "NetAuthMan Domain Controller Service",
        "version": "1.0.0",
        "description": "IP listener driver",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0,
        "functions": []
    }


def onRequest(path: str, params: dict[str, str], httpSession) -> tuple[int, str, str]:
    stdio.println(f"Received request: {path}", tty=3)
    return 200, "text/plain", "Hello, world! Parameters: " + str(params)

def run():
    try:
        stdio.println("Starting NetAuthMan Domain Controller Service...")
        KernelSpace.syscall("drv.serverinfra.iplistener", "addRoute", "/nethman", onRequest)
    except Exception as e:
        stdio.println(f"An error occurred: {e}")
