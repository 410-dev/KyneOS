
# class JournalingContainer:
#
#     journals = {
#         "_global": {
#             "scriptPath": "_",
#             "entries": []
#         },
#         "_registry_access_records": {
#             "scriptPath": "kernel.registry",
#             "entries": []
#         }
#     }
#
#     @staticmethod
#     def addJournal(journal, scriptPath):
#         JournalingContainer.journals[journal] = {
#             "scriptPath": scriptPath,
#             "entries": []
#         }
#
#     @staticmethod
#     def addEntry(journal, entry, maxSize: int = 16384):
#         JournalingContainer.journals[journal]["entries"].append(entry)
#         while len(JournalingContainer.journals[journal]["entries"]) > maxSize:
#             JournalingContainer.journals[journal]["entries"].pop(0)
#
#     @staticmethod
#     def getJournal(journal):
#         return JournalingContainer.journals[journal]
#
#     @staticmethod
#     def getJournalAsString(journal):
#         journalData = JournalingContainer.journals[journal]
#         journalString = f"Script Location: {journalData['scriptPath']}\n"
#         for entry in journalData["entries"]:
#             journalString += entry
#         return journalString
#
#     @staticmethod
#     def dump(to: str = None) -> str:
#         import json
#         if to is None:
#             to = f"{PartitionMgr.etc()}/journals/dump@{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
#         os.makedirs(os.path.dirname(to), exist_ok=True)
#         with open(to, "w") as f:
#             json.dump(JournalingContainer.journals, f, indent=4)
#         return to

import datetime

def record(state: str, text: str):

    # import kernel.registry as Registry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{state}] {text}")
    # caller = traceback.extract_stack(None, 2)[0]
    #
    # # callerName = caller.name
    # scriptPath = caller.filename.replace("//", "/").replace("\\", "/").replace(os.path.abspath(PartitionMgr.root()).replace("//", "/").replace("\\", "/"), "")
    # scriptBundleScope = scriptPath.split("/")[-2] + "." + scriptPath.split("/")[-1].replace(".py", "")
    #
    # # if "<" in callerName or "main" == callerName or "mainAsync" in callerName:
    # #     bundleName = os.path.dirname(caller.filename).replace("//", "/").replace("\\", "/").split("/")[-1]
    # #     scriptFileName = os.path.basename(caller.filename).replace(".py", "")
    # #     callerName = f"{bundleName}.{scriptFileName}"
    #
    # callerName = scriptBundleScope
    # specificJournal = f"{PartitionMgr.etc()}/journals/{Clock.getStartTime().split(".")[0]}/{callerName}.journal"
    # globalJournal = f"{PartitionMgr.etc()}/journals/{Clock.getStartTime().split(".")[0]}/_.journal"
    #
    # if Registry.read("SOFTWARE.CordOS.Kernel.EnableStdoutJournaling", default="0") == "1":
    #     print(f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}")
    #
    # if Registry.read("SOFTWARE.CordOS.Kernel.DisableOnMemoryJournaling", default="0") == "0":
    #     if callerName not in JournalingContainer.journals:
    #         JournalingContainer.addJournal(callerName, scriptPath)
    #     JournalingContainer.addEntry(callerName, f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
    #     JournalingContainer.addEntry("_global", f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
    #
    #     maxSize = int(Registry.read("SOFTWARE.CordOS.Kernel.OnMemoryJournalingMaxEntryPerProcess", default="16384"))
    #     while len(JournalingContainer.journals[callerName]["entries"]) > maxSize:
    #         JournalingContainer.journals[callerName]["entries"].pop(0)
    #
    # if Registry.read("SOFTWARE.CordOS.Kernel.EnableOnDiskJournaling", default="0") == "1":
    #     # Create directory
    #     directory = os.path.dirname(specificJournal)
    #     os.makedirs(directory, exist_ok=True)
    #
    #     # Write to file if not exists
    #     if not os.path.exists(specificJournal):
    #         with open(specificJournal, "w") as f:
    #             f.write(f"Script Location: {scriptPath}\n")
    #             f.write(f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
    #     else:
    #         with open(specificJournal, "a") as f:
    #             f.write(f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
    #
    #     if not os.path.exists(globalJournal):
    #         with open(globalJournal, "w") as f:
    #             f.write(f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
    #     else:
    #         with open(globalJournal, "a") as f:
    #             f.write(f"[{timestamp}] [{state}] [{caller.name}@{callerName}] {text}\n")
