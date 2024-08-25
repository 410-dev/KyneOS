# KyneOS
A robust successor of NanoPyOS lineage.

## What is KyneOS?
KyneOS is a pseudo-OS written in Python, handling various services and tasks for certain purpose. The best example of the usage of KyneOS is hosting the service as Discord bot.

The reason that Discord bot could be a good example is that KyneOS supports background tasks, event driven trigger, built-in multiuser support with directory service, scalable functionalities and even policy management.

## What is better than NanoPyOS / CordOS?

NanoPyOS (CordOS) is primarily designed for Discord bot but has been extended its feature as pseudo-os. However, this led to lack of many of the features described above. Some of them are implemented during incremental updates, but some functionalities could not be implemented due to its native limitation.

KyneOS is fundamentally rewritten from scratch, and designed to be more robust and scalable with higher modularity. It certainly is more complex than NanoPyOS, but the trade-off is worth it.

### Security
Nearly all the kernel components were fully accessible by user and third party softwares without limitation, and could be executed directly. After NanoPyOS allowed third-party software installation from Git, this became a significant security risk. KyneOS has a strict policy to prevent this kind of security risk.

KyneOS has separated kernelspace and userspace, and only the kernelspace has the privilege to access the system resources. The userspace is isolated from the kernelspace, and the userspace can only access the kernelspace through the system call interface.

### Stability
NanoPyOS supports background process, but was highly dependent on IPC (Inter-Process Communication) and was lack of central control. This led to frequent system unresponsiveness, especially when the system is shutting down or restarted because the kernel could not forcefully terminate the process.

KyneOS now enforces the process management, and the kernel has the privilege to terminate the process, which can lead to more stable system, like exception handling, journaling, and service management.

### Modularity
Due to NanoPyOS's nature, the modularity was limited and extremely complex. Even if the module was created, it is not guaranteed to work for all features. This led to lack of extensibility of features and controls.

KyneOS has a more modular design, and the system is divided into multiple services and applications. Each service and application is independent and can be added or removed without affecting other services and applications. This leads to more extensibility and control.

### Maintainability
NanoPyOS used tree structured configuration system like registry, which was good for simple use, but eventually led to cluttered configuration and lack of modularity.

KyneOS uses configuration based on JSON, which is more human-readable and easier to maintain. The configuration files are separated by each service and applications, and even could be separated per features. This leads to more modular and maintainable configuration.

### Safety
NanoPyOS didn't have centralized authorization unit and was lack of policy management, which lead to logon vulnerabilities and fragmentation.

KyneOS has AuthMan authorization unit with NethMan interface for authorization over network, and supports policy management using Directory Service.

### New features
- **Directory Service**: Centralized user and group management system.
- **Remote Management Service**: Like SSH, KyneOS could be controlled remotely once connection is authorized.
- **AuthMan / NethMan**: Authorization unit for both internal and external authorization.