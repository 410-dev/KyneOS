# NanoPyOS Backend

## Introduction

This is a documentation related to NanoPyOS backend for legacy support. Check out [Legacy Support Policy ](Legacy%20Support%20Policy.md) for more information about legacy support.

## How it works

Most cases that requires NanoPyOS backend requires to import `kernel` package in the root of the system. KyneOS, however, already has further developed standard in structuring the directories and libraries for higher maintainability. This means `kernel` package is no longer available in the root directory.

## Installing NanoPyOS Backend

The installation could be done through the following commandline in KyneUI.

Installing from built-in package (Recommended)

```
framework /System/Library/Frameworks/NanoPyOSBackend task=install usingInternal=true
```

Installing from external source

```
framework /System/Library/Frameworks/NanoPyOSBackend task=install usingInternal=false manifest=<manifest_file_in_url_format>
```

The manifest file should be passed in as URL format. The supported URL protocols are `http`, `https`, `file`.

Manifest file should keep the following format.

```json
{
  "manifest": "Manifest for NanoPyOS Backend on KyneOS installation",
  "profile": {
    "kernel": "1.0",
    "build": "240604.indev-stable.1"
  },
  "install": {
    ""
  }
}
```

