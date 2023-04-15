# imports for main file
from flet import *
from pages.authentication.forgotPassword import ForgotPassword
# importing views that contain routes for all the pages.
from pages.home import Home
from pages.authentication.login import Login
from pages.pageNotFound import pageNotFound
from pages.profile import userProfile
from pages.serverError import serverError
from pages.authentication.signup import Signup
from pages.booking_request import BookingRequest
from pages.requestHistory import RequestHistory
from pages.admin_control.approveRequest import ApproveRequest
from pages.admin_control.vehicleDetails import VehicleDetail

# Main function of the website that will run the entire website.
# Views that have control over all other pages is linked to this function


def main(page: Page):
    page.bgcolor = colors.DEEP_PURPLE_100
    page.title = "Book my trip"
    page.theme_mode = "dark"
    
    


    # function for the route change. It calls a views_handler to change for the routes.
    def route_change(route):
        page.views.clear()
        # page.views.append(Home(page))
        
        routeParm = page.route
        match routeParm:
            case "/login" : page.views.append(Login(page))
            case "/home" : page.views.append(Home(page))
            case "/signup": page.views.append(Signup(page))
            case "/bookingRequest": page.views.append(BookingRequest(page))
            case "/requestHistory": page.views.append(RequestHistory(page))
            case "/approveRequest": page.views.append(ApproveRequest(page))
            case "/vehicleDetail": page.views.append(VehicleDetail(page))
            case "/user/profile" : page.views.append(userProfile(page))
            case "/pageNotFound" : page.views.append(pageNotFound(page))
            case "/serverNotFound" : page.views.append(serverError(page))
            case "/forgotPassword" : page.views.append(ForgotPassword(page))
                 
    page.update()

    # pop function for route if user wants to go back.
    

    
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # calling on route change method for route change
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # rroute to the first page on startup
    isAuth = page.client_storage.get("isAuthenticated")
    if isAuth:
        page.go("/home")
    else:
        page.go("/login")


# refrencing app to run the main file.
# setting ports , view and asset directory
app(target=main, port=8080, view= WEB_BROWSER, assets_dir="assets")
