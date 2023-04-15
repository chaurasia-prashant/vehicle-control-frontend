import os
from flet.security import encrypt,decrypt


from dotenv import load_dotenv
load_dotenv()
secreat_key = os.environ["SECREAT_KEY"]

# local storage for user

# function to set user data to local storage that can be accessiable from any page
# triggers on user successful registration or login.





def setUserData(page, userData):
    try:
        pref = page.client_storage
        pref.set("username",encrypt(userData["username"],secreat_key))
        pref.set("email",encrypt(userData["email"],secreat_key) )
        pref.set("empId",encrypt(userData["empId"],secreat_key) )
        pref.set("department",encrypt(userData["department"],secreat_key) )
        pref.set("phoneNumber",encrypt(userData["phoneNumber"],secreat_key) )
        pref.set("isAuthorized",encrypt(str(userData["isAuthorized"]),secreat_key))
        pref.set("verifyPhoneNumber",encrypt(str(userData["verifyPhoneNumber"]),secreat_key))
        pref.set("verifyEmail",encrypt(str(userData["verifyEmail"]),secreat_key) )
        pref.set("isOwner",encrypt(str(userData["isOwner"]),secreat_key) )
        pref.set("isAdmin",encrypt(str(userData["isAdmin"]),secreat_key) )
        
        pref.set("uid", userData["uid"])
    except:
        return "error"

# function to get user data that are stored in local storage.
# Can be access from any page of this website.
def getBool(data):
    if data == "True":
        return True
    else:
        return False

def getUserData(page):
    pref = page.client_storage
    data = {}
    try:
        data["username"] = decrypt( pref.get("username"), secreat_key)
        data["email"] =decrypt( pref.get("email"), secreat_key)
        data["empId"] =decrypt( pref.get("empId"), secreat_key)
        data["department"] =decrypt( pref.get("department"), secreat_key)
        data["phoneNumber"] =decrypt( pref.get("phoneNumber"), secreat_key)
        data["isAuthorized"] = getBool(decrypt( pref.get("isAuthorized"), secreat_key))
        data["verifyPhoneNumber"] =getBool(decrypt( pref.get("verifyPhoneNumber"), secreat_key))
        data["verifyEmail"] = getBool(decrypt( pref.get("verifyEmail"), secreat_key))
        data["isOwner"] = getBool(decrypt( pref.get("isOwner"), secreat_key))
        data["isAdmin"] = getBool(decrypt( pref.get("isAdmin"), secreat_key))
        data["uid"] = pref.get("uid")
        
        return data
    except:
        page.client_storage.set("isAuthenticated", False)
        page.update()
    
    


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