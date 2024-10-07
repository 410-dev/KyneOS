# Legacy Support Policy


## Introduction
As system grows, there may be some codes or libraries that may deprecate. This is a common issue in software development. This document is for defining the general policy of KyneOS development in terms of treating legacy support of the internal SDK.

## General Policy
KyneOS will not generally support or guarantee the support of the legacy SDKs. This means once an SDK or API is marked as deprecated, it will be removed in the next major release with warning in runtime before removal. Any SDKs that are not marked as deprecated will not be removed in the near future.

However, the general usage or implementation standard will be kept as much as possible so that to some extent, developers or users may add extra support for the deprecated SDKs as an extension form. Additional extensions installation policy could be found in [extra software policy](Extra%20Software%20Policy.md), and installation guide could be found in [extra software installation guide](Installing%20Software.md).

## Deprecation Policy
When an SDK or API is marked as deprecated, the related documentation will be tagged as `Deprecated`. The deprecated SDK or API will be removed in the next major release. The deprecated SDK or API will be kept in the system for at least 1 year after the deprecation.

However, some SDKs or APIs could be blacklisted from kernel due to sensitive issues such as security or integrity issues. In this case, the documentation will be tagged as `Vulnerable`, and specific implementation or example codes will be fully removed.

## Nano Kernel Support

#### General Statement

Default NanoPyOS kernel will be provided as-is without modification if necessary. This means that programs that requires NanoPyOS/CordOS backend will generally operate in KyneOS as it worked on NanoPyOS/CordOS. However, some programs that are heavily dependent on NanoPyOS backend is not guaranteed to work as expected. The NanoPyOS kernel will not be included out of the box based on the general policy of legacy support policy. NanoPyOS backend could be installed by following [NanoPyOS Backend](NanoPyOS%20Backend.md) documentation.

#### Update Policy

Nano kernel support will NOT be thoroughly tested and will NOT frequently update. Some portion of the kernel source code could be modified for compatibility, such as hard coded location of system file location or partition mappings. For this reason, NanoPyOS backend could not be updated frequently and efficiently.

#### Behavior

Any `import` statement that is trying to import from `kernel.*` will be redirected to currently installed NanoPyOS kernel backend, such as `/Library/LegacySupport/NanoPyOS/` or `/System/NanoKernel`.

