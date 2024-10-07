# meta.json Implementation

## Example Structure
```json
{
    "Bundle": "KyneOS:Framework:1.0",
    "DisplayName": "OSProfiler",
    "ProcessName": "OSProfiler",
    "Description": "KyneOS Versioning Profile Manager",
    "Attributes": {
        "Priority": 0,
        "Type": "frmwrk",
        "Class": "kyne",
        "Id": "osprofiler",
        "Name": "OSProfiler",
        "Version": "1.0",
        "Distro": "Universal",
        "ExplicitCompatibility": {
            "SDK": ["1.0", "1.1", "1.2"],
            "API": ["1.0", "1.1", "1.2"],
            "OSVersion": "1.0.0",
            "OSBuild": "1300",
            "OSName": "KyneOS",
            "OSDistro": "Automatic"
        }
    },
    "Runtime": {
        "SupportedArchitecture": ["arm64", "amd64"]
    }
}
```
Each keys in the metadata file are explained below:
- `Bundle`: The bundle type. The basic structure looks `KyneOS:<Type>:<Version>`. The type can be `Framework`, `Application`, `Service`, `Driver`, `Extension`, `Event`. This is used to check bundle compatibility
- `DisplayName`: The name of the bundle that will be displayed in the system.
- `ProcessName`: The name of the process that will be executed. This name will be registered to kernel process management system.
- `Description`: A brief description of the bundle.
- `Attributes`: The attributes of the bundle. Data in here could be retrieved by implementation of [Bundle object](../System%20Objects/Bundle.md), using `bundle.getAttributes()` or `bundle.getAttributeOf(<key>)`.
    - [Extension / Service] `Priority`: The priority of the bundle. The priority is used to determine the order of execution of the bundles. The lower the number, the higher the priority.
    - [Universal] `Type`: The type of the bundle. This can be `frmwrk`, `app`, `service`, `driver`, `extension`, `event`.
    - [Universal] `Class`: The class of the bundle. This can be organization name such as `microsoft`, `apple`, `google`. However, for some low-level bundles, this could be something like `io`, `sys`, `dev`.
    - [Universal] `Id`: The unique identifier of the bundle.
    - [Universal] `Name`: The name of the bundle. This is displayed in the system and users can see this name.
    - [Universal] `Version`: The version of the bundle.
    - [Universal] `Distro`: The system distro that this bundle is supported: `Universal`, `Desktop`, `Server`. This is used to check bundle compatibility.
    - [Optional] Any other data could be added to the `Attributes` object that could be later retrieved by the bundle implementation. In the example above, the `ExplicitCompatibility` object is added to check compatibility with the system.
    - [Optional for Framework] `ResourceLocks`: This is a list of keys that will prevent [framworksupport (Including `System.framework`)](../../About%20System/Extensions/frameworksupport.md) from accessing the the resource.
- `Runtime`: The runtime attributes of the bundle. This is used to check compatibility with the host system.
    - `SupportedArchitecture`: The supported architecture of the bundle. This could be `arm64`, `amd64`, `universal`.
    - [Optional] `SupportedHost`: The supported host OS of the bundle. This could be `nt`, `linux`, `darwin`.
    - [Optional] `RequiredMinimumPythonVersion`: The required Python version of the bundle. This is used to check compatibility with the system.
    - [Optional] `RequiredPythonPackages`: The required Python packages of the bundle. This is used to check compatibility with the system.
