from datetime import datetime
import flet as ft
import requests
from database.getFromDb import getAllBookkingRequest
from user_controls.app_bar import Navbar
from user_controls.urls import urls

# View for approving a user's travel request
# this page is controlled only by admin
# To approve a request admin have to fill vehicle details and remarks.

def ApproveRequest(page: ft.page):
    
    allRequests = getAllBookkingRequest()

    # function to enable approving form for admin.
    
    
    def showFinalApprovePopUp(e,reqId,id):
        if id == 1:
            actionButton.text ="Final Approve"
            actionButton.on_click = approveByAdmin
            actionButton.update
        else:
            vehicleDetail.visible = False
            vehicleDetail.update()
            actionButton.text ="Final Reject"
            actionButton.on_click = rejectByAdmin
            actionButton.update    
        bookingId.value = reqId
        bookingId.update()
        approveScreen.visible = None
        approveScreen.visible = True
        approveScreen.update()
        # page.update()
    # function to disable approving form.

    def closeFinalApprovePopUp(e):
        vehicleDetail.visible = True
        vehicleDetail.update()
        approveScreen.visible = None
        approveScreen.visible = False
        approveScreen.update()
        errMessage.visible =False
        errMessage.update()
        # page.update()
    
    vehicleDetail =ft.TextField(
                    label="Vehicle Number",
                    color=ft.colors.WHITE,
                    height=50,
                    border_color=ft.colors.BLUE,
                )    
    remark =ft.TextField(
                    label="Remark",
                    color=ft.colors.WHITE,
                    multiline=True,
                    max_lines=3,
                    max_length=100,
                    border_color=ft.colors.BLUE,
                )
    errMessage =ft.Text(
        "All fields are mandatory",
        visible=False,     
        color= ft.colors.RED_ACCENT_200)       
    def approveByAdmin(e):
        data = {
            "vehicleAlloted": "jh20",
            "vehicleNumber": vehicleDetail.value,
            "tripStatus": True,
            "tripCanceled": False,
            "remark": remark.value,
        }
        if vehicleDetail.value and remark.value != "":
            try:
                url =urls()
                url =url["approveRequest"]
                res = requests.put(f"{url}{bookingId.value}",json=data)
                if res.status_code == 200 and res.text != "404":
                    approveScreen.visible = None
                    approveScreen.visible = False
                    approveScreen.update()
                    page.go("/home")
    
            except Exception as e:
                approveScreen.visible = None
                approveScreen.visible = False
                approveScreen.update()
                page.go("/serverNotFound")
        else:
            errMessage.visible =True
            errMessage.update()
            
    def rejectByAdmin(e):
        data = {
            "vehicleAlloted": None,
            "vehicleNumber": None,
            "tripStatus": False,
            "tripCanceled": True,
            "remark": remark.value,
        }
        if remark.value != "":
            try:
                url =urls()
                url =url["rejectRequest"]
                res = requests.put(f"{url}{bookingId.value}",json=data)
                if res.status_code == 200 and res.text != "404":
                    approveScreen.visible = None
                    approveScreen.visible = False
                    approveScreen.update()
                    page.go("/home")
    
            except Exception as e:
                approveScreen.visible = None
                approveScreen.visible = False
                approveScreen.update()
                page.go("/serverNotFound")
        else:
            errMessage.visible =True
            errMessage.update()

    # Approve request's card.
    def requestCard(reqId,reqBy,origin,destination,start,end,date):
        id1 = 1
        id2 = 0
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
                                color=ft.colors.WHITE70,
                                on_click=lambda e: showFinalApprovePopUp(e,reqId,id2)

                            ),
                                ft.Container(width=10),
                                ft.ElevatedButton(
                                "Approve",
                                expand =True,
                                bgcolor=ft.colors.GREEN_900,
                                color=ft.colors.WHITE70,
                                on_click= lambda e:showFinalApprovePopUp(e,reqId,id1)
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

    reqData = ft.ListView(spacing=10)
    if allRequests != None:
        for res in allRequests:
            if not res["tripStatus"]:
                if not res["tripCanceled"]:
                    date = datetime.strptime(res["tripDate"], "%Y-%m-%dT%H:%M:%S.%f")
                    reqData.controls.append(requestCard(
                        reqId= res["bookingNumber"],
                        reqBy = res["empUsername"], 
                        origin = res["startLocation"],
                        destination= res["destination"],
                        start= res["startTime"],
                        end= res["endTime"],
                        date= date.date()
                        
                    ))
    bookingId = ft.Text("Booking Number")
    actionButton =ft.ElevatedButton(
                        # "Final Approve",
                        bgcolor=ft.colors.GREEN_900,
                        # on_click=approveByAdmin
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
                errMessage,
                ft.Row([
                    ft.Text("Booking Number: "),
                    bookingId,
                ]),
                
                vehicleDetail,
                remark,
                ft.Row([
                    ft.ElevatedButton(
                        "Close",
                        bgcolor=ft.colors.RED_900,
                        on_click=closeFinalApprovePopUp
                    ),   actionButton
                ]),

            ],
            )
        )
    )

    approveMainScreen = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 6, "xl": 4},
                height=.9*page.height,
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
                            f"/approve.png",
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
