# Bundle (Executable Structure)
KyneOS supports bundle structure for executable items. This is highly recommended for those who require supplementary resources for their execution.

## Structure
```
<Bundle Name>/
    meta.json
    main.py (or framework.py if bundle is a framework bundle)
    resources/
        <Resource Files>
```

### Bundle name
The name of the bundle should be the name of the executable item. This can be anything.

### meta.json
This file follows KyneOS default [meta.json](meta.json.md) structure.

### `main.py` for Application
This is the main executable file of the bundle. This file will be executed when the bundle is called. For executable application, look for the [execution script implementation](Execution%20Script.md)

`bundle.getExecutable()` will point to this file.

### `main.py` for Extension / Drivers
The main.py for extension or drivers works differently from the application.
main.py file should contain various functions that will be called by the system when the extension or driver is loaded.
The function could be called using [System Calls](../System%20Libraries/System.syscall.md).

### Resources (`resources/`)
This directory contains the resources required for the bundle to execute. This can be anything from images to configuration files.

### Resources for Framework (`resources/`)
This directory contains the resources required for the framework bundle to execute. This can be anything from images to configuration files. 

**Note**: All the files that are not specified in `ResourceLocks` in `meta.json` will be accessible by the [framworksupport (Including `System.framework`)](../../About%20System/Extensions/frameworksupport.md).


## Bundle Example Files
- [Application] [KyneUI](../../../../UserInterfaces/KyneUI) located at `/System/UserInterfaces/KyneUI`
- [Framework] [Installer](../../../../Library/Frameworks/Installer) located at `/System/Library/Frameworks/Installer`
- [Extension] [AuthMan](../../../../Library/Extensions/AuthMan) located at `/System/Library/Extensions/AuthMan`
- 