import flet as ft

# function for the navbar that we using in the website for easy access to
# home screen from any page and logout activity.


def Navbar(page, ft=ft):

    NavBar = ft.AppBar(
        leading=ft.Icon(ft.icons.TAG_FACES_ROUNDED),
        leading_width=40,
        title=ft.Text("BOOK MY TRIP"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/home')),
            ft.IconButton(ft.icons.LOGOUT_ROUNDED,
                          on_click=lambda _: page.go('/')),


        ]
    )

    return NavBar
