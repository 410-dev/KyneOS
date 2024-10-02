# Overwrite kynekernel
# CURRENT_SYS_DISTRO = "Desktop"
# CURRENT_KRNL_NAME = "Kyne"
# CURRENT_KRNL_VERSION = "1.0.0"
# CURRENT_KRNL_TESTVRS = "alpha 1"
# From bundle meta.json

from System.Library.Objects.Bundle import Bundle

def main(args: dict, process) -> dict:
    currentBundle: Bundle = Bundle("/System/Library/Frameworks/OSProfiler")
    properties = currentBundle.getAttributeOf("ExplicitCompatibility")

    returningProps: dict = {}
    if len(args.keys()) == 0:
        returningProps = properties

    elif "get" in args.keys():
        # value structure: OSDistro,OSVersion,SDK
        fieldsToGet: list[str] = args["get"].split(",")
        for field in fieldsToGet:
            if field in properties.keys():
                returningProps[field] = properties[field]
            else:
                returningProps[field] = None

    elif "compatible" in args.keys():
        # value structure: OSDistro:Desktop,API:1.0,OSVersion:1.0.0,SDK:1.0
        # Returns true or false for each field
        compatibility: list[str] = args["compatible"].split(",")
        for comp in compatibility:
            compParts: list[str] = comp.split(":")
            if compParts[0] in properties.keys():
                if isinstance(properties[compParts[0]], str):
                    returningProps[compParts[0]] = properties[compParts[0]] == compParts[1]
                elif isinstance(properties[compParts[0]], list):
                    returningProps[compParts[0]] = compParts[1] in properties[compParts[0]]
                else:
                    returningProps[compParts[0]] = properties[compParts[0]] == compParts[1]
            else:
                returningProps[compParts[0]] = False

    return returningProps
