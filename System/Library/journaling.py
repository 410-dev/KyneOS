
import datetime
import inspect
import hashlib

from System.Library.execspaces import KernelSpace

import System.stdio as stdio
import System.fs as fs

class JournalingContainer:

    journals = {
        "_global": {
            "execPath": "_",
            "entries": []
        },
        "_registry_access_records": {
            "execPath": "kernel.registry",
            "entries": []
        }
    }

    journalLocation = "/Library/etc/journals"

    @staticmethod
    def addJournal(journal, execPath):
        JournalingContainer.journals[journal] = {
            "execPath": execPath,
            "entries": []
        }

    @staticmethod
    def addEntry(journal, entry, maxSize: int = 16384):
        JournalingContainer.journals[journal]["entries"].append(entry)
        while len(JournalingContainer.journals[journal]["entries"]) > maxSize:
            JournalingContainer.journals[journal]["entries"].pop(0)

    @staticmethod
    def getJournal(journal):
        return JournalingContainer.journals[journal]

    @staticmethod
    def getJournalAsString(journal):
        journalData = JournalingContainer.journals[journal]
        journalString = f"Script Location: {journalData['execPath']}\n"
        for entry in journalData["entries"]:
            journalString += entry
        return journalString

    @staticmethod
    def dump(to: str = None) -> str:
        import json
        if to is None:
            to = f"{JournalingContainer.journalLocation}/dump@{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        # os.makedirs(os.path.dirname(to), exist_ok=True)
        fs.makeDir("/".join(to.split("/")[:-1]))
        with open(to, "w") as f:
            json.dump(JournalingContainer.journals, f, indent=4)
        return to


def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "kyne",
        "id": "journaling",
        "name": "Journaling",
        "version": "1.0.0",
        "description": "Journaling",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 1000
    }


def record(state: str, text: str):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    frame = inspect.currentframe()
    process = None
    callerFunctionTraces = []
    while frame:
        frame_info = inspect.getframeinfo(frame)
        callerFunctionTraces.append(frame_info.function)
        if 'System/Library/Objects/Process.py' in frame_info.filename:
            # Now check for any instance of the Process class in the local variables
            local_vars = frame.f_locals
            process = local_vars.get('self')  # This should get process object
            # print(f"exec: {selfObject.executable}")
            break
        else:
            # Move to the previous frame in the call stack
            frame = frame.f_back

    sTime: str = f"{KernelSpace.syscall("ext.time.clock", "getStartupTime")}"
    execPath = process.executable

    # If caller is a bundle format, get the bundle path
    execParent = "/".join(execPath.split("/")[:-1])
    if fs.isFile(f"{execParent}/meta.json"):
        execPath = execParent

    simpleName = execPath.split("/")[-1]
    callerFunction = callerFunctionTraces[1] # One higher than the current function
    specificJournal = f"{JournalingContainer.journalLocation}/{sTime}/{hashlib.md5(execParent.encode()).hexdigest().encode('utf-8')}_{simpleName}.journal"
    globalJournal = f"{JournalingContainer.journalLocation}/{sTime}/_.journal"

    if process is None or process.ownerUser is None:
        prefDat: dict = {
            "EnableStdoutJournaling": True,
            "EnableDiskJournaling": False,
            "DisableMemoryJournaling": False
        }
    else:
        prefDat: dict = process.ownerUser.getPreferenceOf("me.lks410.journaling")

    if prefDat.get("EnableStdoutJournaling", False):
        stdio.println(f"[{timestamp}] [{state}] [{simpleName}] {text}")
    
    if prefDat.get("DisableMemoryJournaling", False):
        if simpleName not in JournalingContainer.journals:
            JournalingContainer.addJournal(simpleName, execPath)
        JournalingContainer.addEntry(simpleName, f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")
        JournalingContainer.addEntry("_global", f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")

        maxSize = int(prefDat.get("MemoryJournalingMaxSize", 8192))
        while len(JournalingContainer.journals[simpleName]["entries"]) > maxSize:
            JournalingContainer.journals[simpleName]["entries"].pop(0)

    if prefDat.get("EnableDiskJournaling", True):
        # Create directory
        directory = "/".join(specificJournal.split("/")[:-1])
        fs.makeDir(directory)

        # Write to file if not exists
        if not fs.isFile(specificJournal):
            fs.writes(specificJournal, f"Script Location: {execPath}\n")
            fs.appends(specificJournal, f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")

        else:
            fs.appends(specificJournal, f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")

        if not fs.isFile(globalJournal):
            fs.writes(globalJournal, f"Script Location: {execPath}\n")
            fs.appends(globalJournal, f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")
        else:
            fs.appends(globalJournal, f"[{timestamp}] [{state}] [{callerFunction}@{simpleName}] {text}\n")
