import flet as ft

# local storage for user

# function to set user data to local storage that can be accessiable from any page
# triggers on user successful registration or login.


def setUserData(page, userData):
    pref = page.client_storage
    pref.set("username", userData["username"])
    pref.set("email", userData["email"])
    pref.set("empID", userData["empID"])
    pref.set("department", userData["department"])
    pref.set("phoneNumber", userData["phoneNumber"])


# function to get user data that are stored in local storage.
# Can be access from any page of this website.


def getUserData(page):
    pref = page.client_storage
    data = {}
    data["username"] = pref.get("username")
    data["email"] = pref.get("email")
    data["empID"] = pref.get("empID")
    data["department"] = pref.get("department")
    data["phoneNumber"] = pref.get("phoneNumber")
    return data
