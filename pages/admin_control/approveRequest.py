import flet as ft
from user_controls.app_bar import Navbar

# View for approving a user's travel request
# this page is controlled only by admin
# To approve a request admin have to fill vehicle details and remarks.


def ApproveRequest(page: ft.page):

    # function to enable approving form for admin.
    def showFinalApprovePopUp(e):
        approveScreen.visible = None
        approveScreen.visible = True
        approveScreen.update()
        page.update()
    # function to disable approving form.

    def closeFinalApprovePopUp(e):
        approveScreen.visible = None
        approveScreen.visible = False
        approveScreen.update()
        page.update()

    # Approve request's card.
    approveRequestsCard = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(
                            ft.icons.CHECK_CIRCLE,
                            # ft.icons.CIRCLE,
                            size=50,
                            color=ft.colors.GREEN,
                        ),
                        title=ft.Text(
                            "Request Number"),
                        subtitle=ft.ListTile(
                            title=ft.Row([
                                ft.Text("Origin",
                                        size=12),
                                ft.Text("To",
                                        size=12),
                                ft.Text("Destination",
                                        size=12)
                            ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            subtitle=ft.Row([
                                ft.Text("Start",
                                        size=11),
                                ft.Text("To",
                                        size=11),
                                ft.Text("End",
                                        size=11)
                            ],
                                alignment=ft.MainAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Row(
                        [ft.ElevatedButton(
                            "Reject",
                            expand=True,
                            bgcolor=ft.colors.RED_900,
                            color=ft.colors.WHITE70

                        ),
                            ft.Container(width=10),
                            ft.ElevatedButton(
                            "Approve",
                            expand=True,
                            bgcolor=ft.colors.GREEN_900,
                            color=ft.colors.WHITE70,
                            on_click=showFinalApprovePopUp

                        ),
                            ft.Container(width=20)
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            ),
            width=400,
            padding=10,
        )
    )

    # Approve form card for admin
    approveScreen = ft.Container(
        visible=False,
        alignment=ft.alignment.center,
        content=ft.Container(
            width=.3*page.width,
            bgcolor=ft.colors.BLACK87,
            padding=15,
            border_radius=10,
            content=ft.Column([
                ft.Text("Booking Number"),
                ft.Dropdown(
                    label="Vehicle Number",
                    color=ft.colors.WHITE,
                    height=50,
                    border_color=ft.colors.BLUE,
                ),
                ft.TextField(
                    label="Remark",
                    color=ft.colors.WHITE,
                    multiline=True,
                    max_lines=3,
                    max_length=100,
                    border_color=ft.colors.BLUE,
                ),
                ft.Row([
                    ft.ElevatedButton(
                        "Close",
                        bgcolor=ft.colors.RED_900,
                        on_click=closeFinalApprovePopUp
                    ),   ft.ElevatedButton(
                        "Final Approve",
                        bgcolor=ft.colors.GREEN_900
                    ),
                ]),

            ],
            )
        )
    )

    approveMainScreen = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 6, "xl": 4},
                height=page.height,
                content=ft.ListView(
                    controls=[

                        approveRequestsCard,

                    ]
                ),
            ),

            ft.Container(
                col={"xs": 0, "sm": 6, "xl": 6},
                content=ft.Column([
                    ft.Container(
                        height=120,
                        content=ft.Text(
                            "Approve for\nTravel Request",
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
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    approveRequest = ft.View(
        "/approveRequest",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        controls=[
            ft.Stack(
                controls=[
                    approveMainScreen,
                    approveScreen
                ]
            )
        ]
    )

    return approveRequest
