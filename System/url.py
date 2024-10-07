from System.Library.execspaces import KernelSpace

def retrieve(urlString: str, process) -> any:
    return KernelSpace.syscall("ext.sys.urlcalls", "call", urlString, process)

def decodeURLByComponents(urlString: str) -> tuple[str, str, dict[str, str]]:
    protocol: str = urlString.split("://", 1)[0]
    url: str = urlString.split("://", 1)[1].split("?", 1)[0]
    argsRaw: list = urlString.split("?", 1)
    if len(argsRaw) < 2:
        return protocol, url, {}
    args: dict[str, str] = {}
    argsRaw = argsRaw[1].split("&")
    for element in argsRaw:
        splitted: list[str] = element.split("=", 1)
        if len(splitted) < 2:
            args[splitted[0]] = ""
        else:
            args[splitted[0]] = "=".join(splitted[1:])

    return protocol, url, args
