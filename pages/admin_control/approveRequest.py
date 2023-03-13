from datetime import datetime
import flet as ft
import requests
from database.getFromDb import getAllBookkingRequest
from user_controls.app_bar import Navbar

# View for approving a user's travel request
# this page is controlled only by admin
# To approve a request admin have to fill vehicle details and remarks.


def ApproveRequest(page: ft.page):
    
    
    allRequests = getAllBookkingRequest(page)
    

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
        
        
    # def approveByAdmin(e):
        
    #     try:
    #         res = requests.post("/approveRequest/{bookingId}",json=data)
    #     except Exception as e:
    #         print(e)

    # Approve request's card.
    def requestCard(reqBy,origin,destination,start,end,date):
        approveRequestsCard = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            # leading=ft.Icon(
                            #     ft.icons.CHECK_CIRCLE,
                            #     # ft.icons.CIRCLE,
                            #     size=50,
                            #     color=ft.colors.GREEN,
                            # ),
                            title=ft.Text(
                                reqBy),
                            subtitle=ft.ListTile(
                                title=ft.Row([
                                    ft.Text(origin,
                                            size=12),
                                    ft.Text("To",
                                            size=12),
                                    ft.Text(destination,
                                            size=12)
                                ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                subtitle=ft.Row([
                                    ft.Text(start,
                                            size=11),
                                    ft.Text("To",
                                            size=11),
                                    ft.Text(end,
                                            size=11)
                                ],
                                    alignment=ft.MainAxisAlignment.START,
                                )
                            )
                        ),
                        ft.Row(
                            [ft.Text(
                                "Date : ",

                            ),
                                ft.Text(
                                date,

                            ),
                                ft.Container(width=20)
                            ],
                            alignment=ft.MainAxisAlignment.END,
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
                                on_click=lambda _: showFinalApprovePopUp

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
        return approveRequestsCard

    reqData = ft.ListView()
    for res in allRequests:
        date = datetime.strptime(res["tripDate"], "%Y-%m-%dT%H:%M:%S.%f")
        reqData.controls.append(requestCard(
            reqBy = res["empUsername"], 
            origin = res["startLocation"],
            destination= res["destination"],
            start= res["startTime"],
            end= res["endTime"],
            date= date.date()
            
        ))
        
    
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
                        bgcolor=ft.colors.GREEN_900,
                        
                        # on_click=approveByAdmin
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
                content=reqData,
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
