from System.Library.execspaces import KernelSpace

import System.stdio as stdio

def main(args: list, process):
    # hostData: dict = process.getPreferenceOf("Global:me.lks410.kyneos.machineprofile")
    # hostData: dict = {
    #     "system": {
    #         "name": hostData.get("system.name"),
    #         "version": hostData.get("system.version"),
    #         "build": hostData.get("system.build"),
    #         "release": hostData.get("system.release"),
    #         "distro": hostData.get("system.distro")
    #     },
    #     "kernel": {
    #         "name": hostData.get("kernel.name"),
    #         "version": hostData.get("kernel.version"),
    #         "release": hostData.get("kernel.release")
    #     }
    # }
    # args.pop(0)
    #
    # if "--sysdefault" in args:
    hostData: dict = KernelSpace.syscall("ext.sys.profile", "getSystemProfile")

    if "--kernel" in args:
        stdio.println(f"{hostData.get('system').get('name')} {hostData.get('system').get('distro')} {hostData.get('system').get('version')} ({hostData.get('system').get('build')}), on {hostData.get('kernel').get('name')} {hostData.get('kernel').get('version')} ({hostData.get('kernel').get('release')})")
        return 0
    stdio.println(f"{hostData.get('system').get('name')} {hostData.get('system').get('distro')} {hostData.get('system').get('version')} ({hostData.get('system').get('build')})")
