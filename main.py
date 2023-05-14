# imports for main file
import time
import flet as ft
from pages.admin_control.adminPage import AdminControlPage
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


def main(page: ft.Page):
    page.bgcolor = ft.colors.DEEP_PURPLE_100
    page.title = "Book my trip"
    page.theme_mode = "dark"
    # page.on_error = page.views.append(serverError(page))
    
    
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Something Went Wrong!"),
        content=ft.Text("Check Your Internet Connection and try again."),
        actions=[
            ft.TextButton("Close", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
        time.sleep(1.5)
        close_dlg(e)
    


    # function for the route change. It calls a views_handler to change for the routes.
    def route_change(route):
        try:
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
                case "/adminControlPage" : page.views.append(AdminControlPage(page))
                case _: page.views.append(pageNotFound(page))
        except Exception as e:
            print(e)
            open_dlg_modal(e)  
            page.go("/home")      
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
if __name__ == "__main__":
    ft.app(target=main, port=80800, view= ft.WEB_BROWSER, assets_dir="assets")
