# Imports for the view file
# Importing all pages file for the routing

from flet import *
from pages.home import Home
from pages.authentication.login import Login
from pages.pageNotFound import pageNotFound
from pages.serverError import serverError
from pages.authentication.signup import Signup
from pages.booking_request import BookingRequest
from pages.requestHistory import RequestHistory
from pages.admin_control.approveRequest import ApproveRequest
from pages.admin_control.vehicleDetails import VehicleDetail

# Function for the route handling. Refrencing the pages to their route header.


def views_handler(page, route):

    routes = {
        "/": Login(page),
        "/home": Home(page),
        "/signup": Signup(page),
        "/bookingRequest": BookingRequest(page),
        "/requestHistory": RequestHistory(page),
        "/approveRequest": ApproveRequest(page),
        "/vehicleDetail": VehicleDetail(page),
        "/pageNotFound" : pageNotFound(page),
        "/serverNotFound" : serverError(page),
    }

    return routes[route]
