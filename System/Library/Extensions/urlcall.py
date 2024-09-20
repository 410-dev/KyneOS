def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "sys",
        "id": "urlcalls",
        "name": "URL Calls",
        "version": "1.0.0",
        "description": "URL Calls Extension",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }


def call(url: str, process) -> any:
    protocol: str = url.split("://", 1)[0]
    urlAssociation: dict = process.ownerUser.getPreferenceOf("me.lks410.urlassoc")
    import System.shexec as shell
    if protocol in urlAssociation:
        return shell.interpretParameters([
            urlAssociation[protocol],
            url
        ], process)
    else:
        raise Exception(f"Protocol '{protocol}' not found in URL Association")
    