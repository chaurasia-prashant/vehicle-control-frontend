from flet import *
from pages.home import Home
from pages.login import Login
from pages.signup import Signup
from pages.booking_request import BookingRequest
from pages.requestHistory import RequestHistory
from pages.admin_control.approveRequest import ApproveRequest
from pages.admin_control.vehicleDetails import VehicleDetail



def views_handler(page,route):

     routes = {
       "/" : Login(page),
       "/home" : Home(page),
       "/signup" : Signup(page),
       "/bookingRequest" : BookingRequest(page),
       "/requestHistory": RequestHistory(page),
       "/approveRequest": ApproveRequest(page),
       "/vehicleDetail" : VehicleDetail(page),
     }
     
     return routes[route]
        
        
 
 