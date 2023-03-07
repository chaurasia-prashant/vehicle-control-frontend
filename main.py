# imports for main file
from flet import *
# importing views that contain routes for all the pages.
from user_controls.views import views_handler

# Main function of the website that will run the entire website.
# Views that have control over all other pages is linked to this function


def main(page: Page):
    page.bgcolor = colors.DEEP_PURPLE_100

    # function for the route change. It calls a views_handler to change for the routes.
    def route_change(route):
        page.views.clear()
        page.views.append(views_handler(page, page.route))
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
    page.go("/")


# refrencing app to run the main file.
# setting ports , view and asset directory
app(target=main, port=8080, view=WEB_BROWSER, assets_dir="assets")
