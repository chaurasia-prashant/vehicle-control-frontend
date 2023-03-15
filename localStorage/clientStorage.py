import flet as ft

# local storage for user

# function to set user data to local storage that can be accessiable from any page
# triggers on user successful registration or login.




def setUserData(page, userData):
    try:
        pref = page.client_storage
        pref.set("username", userData["username"])
        pref.set("email", userData["email"])
        pref.set("empId", userData["empId"])
        pref.set("department", userData["department"])
        pref.set("phoneNumber", userData["phoneNumber"])
        pref.set("isAuthorized", userData["isAuthorized"])
        pref.set("verifyPhoneNumber", userData["verifyPhoneNumber"])
        pref.set("verifyEmail", userData["verifyEmail"])
        pref.set("isOwner", userData["isOwner"])
        pref.set("isAdmin", userData["isAdmin"])
        
        pref.set("uid", userData["uid"])
    except:
        return "error"

# function to get user data that are stored in local storage.
# Can be access from any page of this website.


def getUserData(page):
    pref = page.client_storage
    data = {}
    data["username"] = pref.get("username")
    data["email"] = pref.get("email")
    data["empId"] = pref.get("empId")
    data["department"] = pref.get("department")
    data["phoneNumber"] = pref.get("phoneNumber")
    data["isAuthorized"] = pref.get("isAuthorized")
    data["verifyPhoneNumber"] = pref.get("verifyPhoneNumber")
    data["verifyEmail"] = pref.get("verifyEmail")
    data["isOwner"] = pref.get("isOwner")
    data["isAdmin"] = pref.get("isAdmin")
    data["uid"] = pref.get("uid")
    
    return data


def resetUserData(page):
    try:
        pref = page.client_storage
        pref.remove("username")
        pref.remove("email")
        pref.remove("empId")
        pref.remove("department")
        pref.remove("phoneNumber")
        pref.remove("isAuthorized")
        pref.remove("verifyPhoneNumber")
        pref.remove("verifyEmail")
        pref.remove("isOwner")
        pref.remove("isAdmin")
        pref.remove("uid")
    except:
        return "error"