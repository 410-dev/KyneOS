# Paths of System

## Core directories
- `/System`: The root directory of the system. This includes kernel files and executables, as well as system libraries and APIs for third-party softwares to access system capabilities.
- `/System/Library`: The kernel of the system lives in here. This includes core components of the system, such as drivers, extensions, frameworks, objects, etc. THIS DIRECTORY SHOULD NOT BE MODIFIED.
- `/Library`: This is where most of the configuration or modifiable system resource files live. Files that are located here are applied / affects the system globally.
- `/Users`: This is where user data is stored. Each user has their own home directory in here.


## Details

### System
- `/System/Applications`: The system related interactive applications are stored here.
- `/System/Drivers`: Critical drivers are stored here. This shouldn't change often, but it can be changed.
- `/System/Exec`: System executables scripts are stored here. This shouldn't change in most of the cases. All of the executable scripts in here could be executed from shell enviornment.
- `/System/Extensions`: Functional kernel extensions are stored here. This shouldn't change often, but it can be changed.
- `/System/Frameworks`: System frameworks are stored here. This shouldn't change often, but it can be changed.
- `/System/NanoSupport`: This directory contains raw nano kernel for legacy executable support. Check out [Legacy Support Policy](Legacy%20Support%20Policy.md) and [NanoPyOS Backend](NanoPyOS%20Backend.md) for more information.
- `/System/Server`
- `/System/Services`
- `/System/UserInterfaces`