import flet as ft
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar

# function for HOME page view.


def Home(page: ft.page):
    
    userData = getUserData(page)

    # home card for user actions
    # function takes value and make card to use multiple times.
    # "isVisible" for diciding who can access this card
    # "avtCont" for giving any icon to avtar circle field content.
    # "titleText" for main title of card
    # "subTitletext" for subtitle
    # "btnText" for button name to take user for the respective page.
    # "pageTo" route header for the respective page.

    def homeCard(isVisible, avtCont, titleText, subTitletext, btnText, pageTo):
        homecard = ft.Card(
            visible=isVisible,
            content=ft.Container(

                content=ft.Column(
                    [
                        ft.ListTile(

                            leading=ft.CircleAvatar(
                                content=avtCont,
                                bgcolor=ft.colors.WHITE,

                            ),
                            title=ft.Text(
                                titleText),
                            subtitle=ft.Text(
                                subTitletext
                            ),

                        ),
                        ft.Row(
                            [ft.TextButton(
                                btnText,
                                on_click=lambda _: page.go(
                                    pageTo),

                            ),],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
        return homecard

    homePage = ft.View(
        "/home",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        col={"sm": 6, "xl": 6},
                        height= .9*page.height,
                        content=ft.ListView(
                            controls=[
                                homeCard(
                                    isVisible=True,
                                    avtCont=ft.Icon(
                                        ft.icons.ACCOUNT_CIRCLE_SHARP,
                                        size=40,
                                        color=ft.colors.RED_900,
                                    ),
                                    titleText=userData["username"],
                                    subTitletext=userData["empId"],
                                    btnText="Profile",
                                    pageTo=None
                                ),
                                homeCard(
                                    isVisible=True,
                                    avtCont=ft.Image(
                                        f"/car.png",
                                        fit=ft.ImageFit.CONTAIN,
                                    ),
                                    titleText="Request a New Trip",
                                    subTitletext=None,
                                    btnText="Create Request",
                                    pageTo="/bookingRequest"
                                ),
                                homeCard(
                                    isVisible=True,
                                    avtCont=ft.Icon(
                                        ft.icons.HISTORY_EDU,
                                        size=30,
                                        color=ft.colors.RED_900,
                                    ),
                                    titleText="Review all Trips",
                                    subTitletext=None,
                                    btnText="Check",
                                    pageTo="/requestHistory"
                                ),
                                homeCard(
                                    isVisible=True,
                                    avtCont=ft.Icon(
                                        ft.icons.ADMIN_PANEL_SETTINGS,
                                        size=30,
                                        color=ft.colors.RED_900,
                                    ),
                                    titleText="Approve request",
                                    subTitletext=None,
                                    btnText="Approve",
                                    pageTo="/approveRequest"
                                ),
                                homeCard(
                                    isVisible=True,
                                    avtCont=ft.Icon(
                                        ft.icons.CAR_CRASH_SHARP,
                                        size=30,
                                        color=ft.colors.RED_900,
                                    ),
                                    titleText="Vehicle Details",
                                    subTitletext=None,
                                    btnText="Status",
                                    pageTo="/vehicleDetail"
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
                                alignment=ft.alignment.center,
                            ),

                            ft.Container(
                                height=500,
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
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]
    )

    return homePage
