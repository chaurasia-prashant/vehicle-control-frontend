import flet as ft
from user_controls.app_bar import Navbar

# Vehicle Detail Page


def VehicleDetail(page: ft.page):

    # Function to show status and booking's of a vehicle
    def showvehicleScreen(e):
        if page.width < 576:
            vehicalBookingScreen.visible = None
            vehicalBookingScreen.visible = True
            vehicalBookingScreen.update()
        page.update()

    # hide vehicle booking history
    def closevehicleScreen(e):

        vehicalBookingScreen.visible = None
        vehicalBookingScreen.visible = False,
        vehicalBookingScreen.update()

    # Vehicle card to show vehicles registered.
    vehicleDetail = ft.Card(
        content=ft.Container(
            content=ft.Row([
                ft.Column(
                    [
                        ft.Row([
                            ft.Text(
                                "Vehicle Number"),
                            ft.Text(
                                "JH000542",
                                color=ft.colors.BLUE
                            ),
                        ]),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Text(
                                "Phone Number"),
                            ft.Text(
                                "9192568365"
                            ),
                        ]),

                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    bgcolor=ft.colors.BLUE_900,
                    border_radius=50,
                    content=ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD_IOS,
                        on_click=showvehicleScreen
                    ),
                )

            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding=10,
        )
    )

    # Card to show vehicle booking history.
    vehicleBookHistory = ft.Container(
        bgcolor=ft.colors.PURPLE_900,
        border_radius=10,
        content=ft.Column(
            [
                ft.Container(
                    content=ft.Row([
                        ft.Text(
                            "Date :",
                            weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "DD-MM-YYYY",
                            weight=ft.FontWeight.BOLD
                        ),
                    ]),
                ),

                ft.Container(height=4),
                ft.Text(
                    "Prashant Kumar Chaurasia"
                ),
                ft.Container(height=2),
                ft.Row([
                    ft.Text(
                        "Department :"),
                    ft.Text(
                        "IMD"
                    ),
                ]),
                ft.Container(height=2),
                ft.Row([
                    ft.Text(
                        "3:50"),
                    ft.Text(
                        "To"
                    ),
                    ft.Text(
                        "5:50"
                    ),
                ]),

            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        padding=20,
    )

    # vehicle booking's screen that display it's history cards in a list view
    vehicalBookingScreen = ft.Container(
        visible=False,
        height=.8*page.height,
        width=.8*page.width,
        bgcolor=ft.colors.BLACK87,
        padding=15,
        border_radius=10,
        content=ft.Column([
            ft.Container(
                height=.65*page.height,
                content=ft.ListView(
                    spacing=3,
                    controls=[
                        vehicleBookHistory,
                    ]
                ),),
            # ft.Container(height= 15),
            ft.ElevatedButton(
                "Close",
                on_click=closevehicleScreen

            )
        ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # vehicle's screen to display all vehicle registered.
    vehicleScreeen = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 6, "xl": 3},
                height=page.height,
                content=ft.ListView(
                    controls=[
                        vehicleDetail,

                    ]
                ),
            ),

            ft.Container(
                margin=30,
                col={"xs": 0, "sm": 5, "xl": 4},
                content=ft.Column([
                    ft.Container(
                        height=120,
                        content=ft.Text(
                            "Vehicle Booking History",
                            size=40,
                            color=ft.colors.BLUE_800
                        ),
                        alignment=ft.alignment.center,
                    ),

                    ft.Container(
                        height=500,
                        col={"xs": 0, "sm": 4, "xl": 2},
                        content=ft.ListView(
                            controls=[vehicleBookHistory]
                        )
                    )
                ])
            )


        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # main view for to contain all cards and screen.
    vehicleDetail = ft.View(
        "/vehicleDetail",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),

        controls=[
            ft.Stack(
                controls=[
                    vehicleScreeen,
                    vehicalBookingScreen
                ]
            )
        ]
    )

    return vehicleDetail
