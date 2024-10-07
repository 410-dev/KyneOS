import importlib
import System.fs as fs

def instructions() -> tuple[dict[str, str], dict[str, str], dict[str, callable]]:
    # This should return a tuple of three dictionaries
    # The first dictionary is human-readable instruction to unique name instruction
    #     Human -> Machine
    # The second dictionary is unique name instruction to human-readable instruction
    #     Machine -> Human
    # The third dictionary is unique name instruction to function

    human_to_machine: dict[str, str] = {}
    machine_to_human: dict[str, str] = {}
    functions: dict[str, callable] = {}

    # Instruction files location
    directory = "/System/Library/Frameworks/Installer/Resources/Compilers/1_0/instruct-modules"

    # Read files
    files = fs.listDir(directory)

    implementationFiles = []
    mappingFiles = []
    for file in files:
        # If .mapping, it's a mapping file
        if file.endswith(".mapping"):
            mappingFiles.append(file)

        # If .py, it's an implementation file
        elif file.endswith(".py"):
            implementationFiles.append(file)

    for file in mappingFiles:
        fileContent = fs.reads(f"{directory}/{file}")
        lines = fileContent.split("\n")
        for line in lines:
            if line == "" or line.startswith("#") or line.startswith("//") or "=" not in line:
                continue
            parts = line.split("=")
            human_to_machine[parts[0]] = parts[1]
            machine_to_human[parts[1]] = parts[0]

    for file in implementationFiles:
        module = importlib.import_module(f"System.Library.Installer.Resources.Compilers.1_0.instruct-modules.{file[:-3]}")
        functions.update(module.functions)

    return human_to_machine, machine_to_human, functions

