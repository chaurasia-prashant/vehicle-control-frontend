import flet as ft
from user_controls.app_bar import Navbar


def BookingRequest(page: ft.page):

    startLocation = ft.TextField(
        label="Start Location",
        color=ft.colors.WHITE,
        height = 50,
        
    )
    destination = ft.TextField(
        label="Destination",
        color=ft.colors.WHITE,
        height = 50,
        
    )
    startTime = ft.TextField(
        label="Start Time",
        color=ft.colors.WHITE,
        height = 50,
       
    )
    endTime = ft.TextField(
        label="End Time",
        color=ft.colors.WHITE,
        height = 50,
        
    )

    bookingRequest = ft.View(
        "/bookingRequest",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        # vertical_alignment = ft.MainAxisAlignment.CENTER,
        # horizontal_alignment = ft.CrossAxisAlignment.CENTER,

        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        width = .4*page.width,
                        col={"sm": 6, "xl": 6},
                        margin = 30,
                        padding =30,
                        bgcolor=ft.colors.BLACK87,
                        border_radius=10,
                        content=ft.Column(

                            [
                                startLocation,
                                destination,
                                startTime,
                                endTime,
                                ft.Container(height = 30),
                                ft.ElevatedButton(
                                    "Send Travel Request",
                                    # height= 20,
                                    width = .4*page.width -30,
                                    bgcolor= ft.colors.WHITE,
                                    color= ft.colors.BLUE
                                )
                            ]
                        ),
                    ),

                    ft.Container(
                        col={"xs": 0, "sm": 6, "xl": 6},
                        content=ft.Column([
                            ft.Container(
                                height=120,
                                content=ft.Text(
                                    "Create a new\nTravel Request",
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
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]
    )

    return bookingRequest
