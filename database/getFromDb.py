import flet as ft
import json
import requests
from localStorage.clientStorage import getUserData
from user_controls.urls import urls

    
def getUserRequestHistory(page):
    try:
        user= getUserData(page)
        userId = user["empId"]
        url =urls()
        url =url["userBookings"]
        res= requests.get(f"{url}{userId}/")
        return json.loads(res.content)
    except Exception as e:
        return None


def getAllBookkingRequest():
    try:
        url =urls()
        url =url["allBookingRequests"]
        res= requests.get(f"{url}")
        return json.loads(res.content)
    except Exception as e:
        return None
    
def getAllVehicles():
    try:
        url =urls()
        url =url["getAllVehicles"]
        res= requests.get(f"{url}")
        return json.loads(res.content)
    except Exception as e:
        return None