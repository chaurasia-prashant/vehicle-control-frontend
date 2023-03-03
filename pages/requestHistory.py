import flet as ft
from user_controls.app_bar import Navbar


def RequestHistory(page: ft.page):

    historyCard = ft.Card(
        content=ft.Container(

            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.icons.CHECK_CIRCLE,
                            #ft.icons.CIRCLE,
                            size=50,
                            color=ft.colors.GREEN,
                        ),
                        title=ft.Text(
                            "Request Number"),
                        subtitle=ft.ListTile(
                            title=ft.Row([
                                ft.Text("Origin",
                                        size = 12),
                                ft.Text("To",
                                        size = 12),
                                ft.Text("Destination",
                                        size = 12)
                            ],
                                alignment= ft.MainAxisAlignment.START,         
                                         ),
                            subtitle= ft.Row([
                                ft.Text("Start",
                                        size = 11),
                                ft.Text("To",
                                        size = 11),
                                ft.Text("End",
                                        size = 11)
                            ],
                                alignment= ft.MainAxisAlignment.START,
                                             )
                        )
                    ),
                    ft.Row(
                        [ft.Text(
                            "Date : ",
                            
                        ),
                         ft.Text(
                            "DD-MM-YYYY",
                            
                        ),
                         ft.Container(width = 20)
                         ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ]
            ),
            width=400,
            padding=10,
        )
    )

    requestHistory = ft.View(
        "/requestHistory",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        # vertical_alignment = ft.MainAxisAlignment.CENTER,
        # horizontal_alignment = ft.CrossAxisAlignment.CENTER,

        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        col={"sm": 6, "xl": 4},
                        content=ft.ListView(

                            controls=[

                                historyCard
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
                                col={"xs": 0, "sm": 4, "xl": 2},
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

    return requestHistory
