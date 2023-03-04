import flet as ft
from user_controls.app_bar import Navbar
from localStorage.clientStorage import getUserData

def Home(page: ft.page):
    
    def getData(e):
        try:
            print(getUserData(page))
        except Exception as e: print(e)

        

    homePage = ft.View(
        "/home",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        # vertical_alignment = ft.MainAxisAlignment.CENTER,
        # horizontal_alignment = ft.CrossAxisAlignment.CENTER,

        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        col={"sm": 6, "xl": 6},
                        content=ft.Column(

                            [
                                ft.Card(
                                    content=ft.Container(

                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    leading=ft.Icon(
                                                        ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                                                        size=50,
                                                        color=ft.colors.WHITE,
                                                    ),
                                                    title=ft.Text(
                                                        "USER NAME"),
                                                    subtitle=ft.Text(
                                                        "USER MAIL ID"
                                                    ),
                                                ),
                                                ft.Row(
                                                    [ft.TextButton(
                                                        "User Profile",
                                                        on_click=lambda _: page.go(
                                                            "/")
                                                    ),],
                                                    alignment=ft.MainAxisAlignment.END,
                                                ),
                                            ]
                                        ),
                                        width=400,
                                        padding=10,
                                    )
                                ),
                                ft.Card(
                                    content=ft.Container(

                                        content=ft.Column(
                                            [
                                                ft.ListTile(

                                                    leading=ft.CircleAvatar(
                                                        content=ft.Image(
                                                            f"/car.png",
                                                            fit=ft.ImageFit.CONTAIN,
                                                        ),
                                                        bgcolor=ft.colors.WHITE,

                                                    ),
                                                    title=ft.Text(
                                                        "Request a new Trip"),

                                                ),
                                                ft.Row(
                                                    [ft.TextButton(
                                                        "Create Request",
                                                        on_click= lambda _: page.go("/bookingRequest"),
                                                        
                                                        ),],
                                                    alignment=ft.MainAxisAlignment.END,
                                                ),
                                            ]
                                        ),
                                        width=400,
                                        padding=10,
                                    )
                                ),
                                ft.Card(
                                    content=ft.Container(

                                        content=ft.Column(
                                            [
                                                ft.ListTile(
                                                    leading=ft.Icon(
                                                        ft.icons.HISTORY_EDU,
                                                        size=50,
                                                        color=ft.colors.WHITE,
                                                    ),
                                                    title=ft.Text(
                                                        "Review all trips"),

                                                ),
                                                ft.Row(
                                                    [ft.TextButton("Check", on_click= getData,
                                                                   ),
                                                     ],
                                                    alignment=ft.MainAxisAlignment.END,
                                                ),
                                            ]
                                        ),
                                        width=400,
                                        padding=10,
                                    )
                                ),

                            ]
                        ),
                    ),
                    
                    ft.Container(
                        col={"xs": 0, "sm": 6, "xl": 6},
                        content=ft.Column([
                            ft.Container(
                                height=120,
                                content=ft.Text(
                                    "Welcome to\nBook My Trip",
                                    size=40,
                                    color=ft.colors.BLUE_800
                                ),
                                alignment = ft.alignment.center,
                            ),

                            ft.Container(
                                height =500,
                                col={"xs": 0, "sm": 5, "xl": 2},
                                content=ft.Image(
                                    f"/car.png",
                                    height=page.height,
                                    width=.5*page.width,
                                    fit=ft.ImageFit.CONTAIN,
                                )
                            )
                        ])
                    )


                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]
    )

    return homePage
