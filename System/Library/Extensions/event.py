import System.fs as fs

def DECLARATION() -> dict:
    return {
        "type": "ext",
        "class": "kyne",
        "id": "eventtrigger",
        "name": "Event Trigger",
        "version": "1.0.0",
        "description": "Triggers events for KyneOS",
        "author": "LKS410",
        "license": "MIT",
        "distro": "Universal",
        "priority": 0
    }

systemEventCache: dict[str, list[str]]
userEventCache: dict[str, dict[str, list[str]]]

def trigger(event: str, process):
    # 1. System
    # 2. User
    # for eventCategory in systemEventCache:
    #     if event in systemEventCache[eventCategory]:
    pass

def updateSysCache():
    # Updates index cache of events

    locations: list[str] = [
        "/System/Events",
        "/System/ServerInfrastructures/Events",
        "/Library/Events",
        "/Library/Server/Events"
    ]
    for location in locations:
        if fs.isDir(location):
            for eventCategory in fs.listDir(location):
                if not fs.isDir(eventCategory):
                    continue  # This is not a category

                for event in fs.listDir(eventCategory):
                    if not fs.isFile(event):
                        continue  # This is not an event file

                    if eventCategory not in systemEventCache:
                        systemEventCache[eventCategory] = []
                    scriptContent = fs.reads(event)
                    systemEventCache[eventCategory].append(scriptContent)
        else:
            continue # This is not a directory


def updateUserCache(userHome: str):
    # Updates index cache of events for user
    # Locations:
    # /Users/*/Events
    if userHome not in userEventCache:
        userEventCache[userHome] = {}

    if fs.isDir(f"{userHome}/Events"):
        for eventCategory in fs.listDir(f"{userHome}/Events"):
            if not fs.isDir(eventCategory):
                continue

            for event in fs.listDir(eventCategory):
                if not fs.isFile(event):
                    continue

                if eventCategory not in userEventCache[userHome]:
                    userEventCache[userHome][eventCategory] = []
                scriptContent = fs.reads(event)
                userEventCache[userHome][eventCategory].append(scriptContent)
    else:
        return

updateSysCache()