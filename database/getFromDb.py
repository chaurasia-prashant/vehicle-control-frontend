import json
import requests
from localStorage.clientStorage import getUserData

    
def getUserRequestHistory(page):
    user= getUserData(page)
    userId = user["empId"]
    res= requests.get(f"http://127.0.0.1:8000/userBookings/{userId}/")
    return json.loads(res.content)


def getAllBookkingRequest(page):
    user= getUserData(page)
    userId = user["empId"]
    res= requests.get(f"http://127.0.0.1:8000/allBookingRequests/")
    return json.loads(res.content)