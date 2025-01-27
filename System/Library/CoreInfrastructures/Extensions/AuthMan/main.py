import hashlib
import random
import time

import System.Library.Security.RSA as RSA
from System.Library.CoreInfrastructures.execspaces import KernelSpace
from System.Library.CoreInfrastructures.Objects.DSObject import DSObject

userValidationQueue: dict[str, dict[str, int|str]] = {
    # "user@localhost#from": {
    #     "expected": "key",
    #     "expireAt": 0
    # }
}

def createUser(username: str, password: str, forest: str, domain: str, directoryRoute: str):
    dc: DSObject = DSObject(f"/{forest}/{domain}")
    authManHash = createAuthManHash(domain, username, password)
    authManPK = mkPublicKey(domain, username, password)
    userData: dict = DSObject.UserObjectData(username, username, username, directoryRoute, "", authManHash, authManPK)
    dc.createObject(f"{directoryRoute}/{username}", userData)

def validateUser(username: str, password: str, forest: str, domain: str, directoryRoute: str) -> tuple[bool, str, DSObject|None]:
    dc: DSObject = DSObject(f"/{forest}/{domain}")
    user: DSObject = dc.getChildObject(f"{directoryRoute}/{username}")
    if user is None:
        return False, "Invalid username or password.", None
    authManHash = createAuthManHash(domain, username, password)

    # Use hash only for validation if local
    if "local" in dc.getName().lower():
        if user.getAttribute("authorization") is None:
            return False, "Error: Unable to load user identity.", None

        if not user.getAttribute("authorization")["AuthManHash"] == authManHash:
            return False, "Invalid username or password.", None

        return True, "Validation successful.", user

    # Use public key for validation if remote
    else:
        return False, "Remote validation requires challenge based authentication.", None


def askChallenge(requestFrom: str, username: str, forest: str, domain: str, directoryRoute: str) -> tuple[bool, str]:
    dc: DSObject = DSObject(f"/{forest}/{domain}")
    user: DSObject = dc.getChildObject(f"{directoryRoute}/{username}")
    if user is None:
        return False, "Invalid username or password."

    if user.getAttribute("authorization") is None:
        return False, "Error: Unable to load user identity."

    authManPK = user.getAttribute("authorization")["AuthManPK"]
    if authManPK is None:
        return False, "Error: Unable to load user identity. (Empty public key)"

    randomStr = "".join([random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(16)])
    challenge = RSA.Encrypt(randomStr, authManPK)
    challengeLiveTimeSeconds = user.getPolicyValue("SystemAdministration.Security.AuthMan.RemoteLogin.ChallengeTimeLiveSeconds", 60)
    userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"] = {
        "expected": randomStr,
        "expireAt": int(time.time()) + challengeLiveTimeSeconds
    }
    return True, challenge


def checkChallenge(requestFrom: str, username: str, challengeResponse: str, forest: str, domain: str, directoryRoute: str) -> tuple[bool, str, DSObject|None]:
    dc: DSObject = DSObject(f"/{forest}/{domain}")
    user: DSObject = dc.getChildObject(f"{directoryRoute}/{username}")
    if user is None:
        return False, "Invalid username or password.", None

    if user.getAttribute("authorization") is None:
        return False, "Error: Unable to load user identity.", None

    if f"{username}@{dc.getDomain()}#{requestFrom}" not in userValidationQueue:
        return False, "Challenge invalid.", None

    if userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"]["expireAt"] < int(time.time()):
        del userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"]
        return False, "Challenge expired.", None

    if userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"]["expected"] != challengeResponse:
        del userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"]
        return False, "Challenge failed.", None

    del userValidationQueue[f"{username}@{dc.getDomain()}#{requestFrom}"]
    return True, "Challenge resolved.", user

def createAuthManHash(domain: str, username: str, password: str) -> str:
    baseStr: str = f"<AuthManHash>DOMAIN={domain};USERNAME={username};PASSWORD={password}</AuthManHash>"
    return hashlib.sha256(baseStr.encode()).hexdigest()

def mkPublicKey(domain: str, username: str, password: str) -> str:
    hashStr = createAuthManHash(username, password, domain)
    return RSA.GetPublicKey(password, hashStr)

def mkPrivateKey(domain: str, username: str, password: str) -> str:
    hashStr = createAuthManHash(username, password, domain)
    return RSA.GetPrivateKey(password, hashStr)
