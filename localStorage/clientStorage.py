import flet as ft

# from models.userModel import UserData

def setUserData(page, userData ):
    pref = page.client_storage
    pref.set("username" , userData["username"])
    pref.set("email" , userData["email"])
    pref.set("empID" , userData["empID"])
    pref.set("department" , userData["department"])
    pref.set("phoneNumber" , userData["phoneNumber"])
        
        
def getUserData(page):
    pref = page.client_storage
    data = {}
    data["username"] = pref.get("username" )
    data["email"] =pref.get("email")
    data["empID"] =pref.get("empID")
    data["department"] =pref.get("department" )
    data["phoneNumber"] =pref.get("phoneNumber" )
    return data