from datetime import datetime
import time
import flet as ft
import requests
from database.getFromDb import getAllBookkingRequest, getAllVehicles
from database.staticData import secondsToTime
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar
from user_controls.urls import urls

# View for approving a user's travel request
# this page is controlled only by admin
# To approve a request admin have to fill vehicle details and remarks.

def ApproveRequest(page: ft.page):
    currentUser = getUserData(page)
    allRequests = getAllBookkingRequest()
    allVehicles = getAllVehicles()
    timeTxt = secondsToTime()
    # function to enable approving form for admin.
    
    
    def showFinalApprovePopUp(e,reqId,id, vechType):
        vehicalListUpdate(e,vechType)
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
    
    vehicleDetail =ft.Dropdown(
                    label="Vehicle Number",
                    color=ft.colors.WHITE,
                    # height=50,
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
    
    def vehicalListUpdate(e,vechType):
        vehicleDetail.options.clear()
        if allVehicles != None:
            for vech in allVehicles:
                if vech["vehicleType"] == vechType:
                    vehicleDetail.options.append(ft.dropdown.Option(vech["vehicleNumber"]))
            page.update()
        
    errMessage =ft.Text(
        "All fields are mandatory",
        visible=False,     
        color= ft.colors.RED_ACCENT_200)       
    def approveByAdmin(e):
        errMessage.visible =False
        errMessage.update()
        data = {
            "vehicleAlloted": vehicleDetail.value,
            "remark": remark.value,
        }
        if vehicleDetail.value and remark.value != "":
            try:
                url =urls()
                url =url["approveRequest"]
                res = requests.put(f"{url}{bookingId.value}/{vehicleDetail.value}",json=data)
                if res.text == "500":
                    errMessage.value = "Something went wrong ! Try again"
                    errMessage.visible =True
                    errMessage.update()
                elif res.text == "904":
                    errMessage.value = "Already Booking For This Time Interval"
                    errMessage.visible =True
                    errMessage.update()    
                    
                elif res.status_code == 200 and res.text != "404":
                    errMessage.value = "Successfully Approved Request"
                    errMessage.color = ft.colors.GREEN_500
                    errMessage.visible =True
                    errMessage.update()
                    time.sleep(.5)
                    # errMessage.visible =False
                    # errMessage.update()
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
            # "vehicleNumber": None,
            # "tripStatus": False,
            # "tripCanceled": True,
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
            
    #Dialoge Box
    def closeDialoge(e):
        dlg_modal.open = False
        page.update()
        
    dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Request Details", size=15, color=ft.colors.BLUE_300),
            actions=[
                ft.TextButton("Close", on_click=closeDialoge),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            # on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
    
    def openDialoge (e,empid, department, reason,isGuest,guestname,guestMobileNum):
        if not isGuest:
            dlg_modal.content = ft.Container(
                content= ft.ResponsiveRow([
                    ft.Text(f"Employee ID : {empid}"),
                    ft.Text(f"Department : {department}"),
                    ft.Text(f"Reason : {reason}")
                ])
            )
        else:
            dlg_modal.content = ft.Container(
                content= ft.ResponsiveRow([
                    ft.Text("Booking For Guest"),
                    ft.Text(f"Employee ID : {empid}"),
                    ft.Text(f"Department : {department}"),
                    ft.Text(f"Guest name : {guestname}"),
                    ft.Text(f"Guest Phone Number : {guestMobileNum}"),
                    ft.Text(f"Reason : {reason}")
                ])
            )
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
        

    # Approve request's card.
    def requestCard(reqId,reqBy,origin,destination,start,end,date,department,reason,id,isGuest,guestname,guestMobileNum,vechType):
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
                            title=ft.Row([
                                
                                ft.Text(reqBy),
                                ft.IconButton(icon= ft.icons.INFO,icon_color=ft.colors.WHITE, on_click= lambda e: openDialoge(e,id,department,reason,isGuest,guestname,guestMobileNum))
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
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
                                on_click=lambda e: showFinalApprovePopUp(e,reqId,id2,vechType)

                            ),
                                ft.Container(width=10),
                                ft.ElevatedButton(
                                "Approve",
                                expand =True,
                                bgcolor=ft.colors.GREEN_900,
                                color=ft.colors.WHITE70,
                                on_click= lambda e:showFinalApprovePopUp(e,reqId,id1,vechType)
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
    if allRequests != [] and allRequests != None:
        for res in allRequests:
            if currentUser["isOwner"] and not currentUser["isAdmin"]:
                if not res["tripStatus"] and res["vehicleType"] == currentUser["department"]:
                    if not res["tripCanceled"]:
                        startTime = res["startTime"]
                        endTime = res["endTime"]
                        reqData.controls.append(requestCard(
                            reqId= res["bookingNumber"],
                            reqBy = res["empUsername"], 
                            origin = res["startLocation"],
                            destination= res["destination"],
                            start= timeTxt[startTime],
                            end= timeTxt[endTime],
                            date= res["tripDate"],
                            id =res["empId"],
                            department= res["userDepartment"],
                            reason= res["reason"],
                            isGuest= res["isGuestBooking"],
                            guestname= res["guestName"],
                            guestMobileNum= res["guestMobileNumber"],
                            vechType= res["vehicleType"],
                            
                        ))
            elif currentUser["isOwner"] and  currentUser["isAdmin"]:
                tb = ["ADMIN",currentUser["department"]]
                if not res["tripStatus"] and res["vehicleType"] in tb:
                    if not res["tripCanceled"]:
                        startTime = res["startTime"]
                        endTime = res["endTime"]
                        reqData.controls.append(requestCard(
                            reqId= res["bookingNumber"],
                            reqBy = res["empUsername"], 
                            origin = res["startLocation"],
                            destination= res["destination"],
                            start= timeTxt[startTime],
                            end= timeTxt[endTime],
                            date= res["tripDate"],
                            id =res["empId"],
                            department= res["userDepartment"],
                            reason= res["reason"],
                            isGuest= res["isGuestBooking"],
                            guestname= res["guestName"],
                            guestMobileNum= res["guestMobileNumber"],
                            vechType= res["vehicleType"],
                            
                        ))
            elif currentUser["isAdmin"]:
                if not res["tripStatus"] and res["vehicleType"] == "ADMIN":
                    if not res["tripCanceled"]:
                        startTime = res["startTime"]
                        endTime = res["endTime"]
                        reqData.controls.append(requestCard(
                            reqId= res["bookingNumber"],
                            reqBy = res["empUsername"], 
                            origin = res["startLocation"],
                            destination= res["destination"],
                            start= timeTxt[startTime],
                            end= timeTxt[endTime],
                            date= res["tripDate"],
                            id =res["empId"],
                            department= res["userDepartment"],
                            reason= res["reason"],
                            isGuest= res["isGuestBooking"],
                            guestname= res["guestName"],
                            guestMobileNum= res["guestMobileNumber"],
                            vechType= res["vehicleType"],
                            
                        ))
    else:
        reqData = ft.Container(padding = 30,content=ft.Text("No Requests Found",
                                        size=50,
                                        color= ft.colors.BLACK))
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
        content=ft.ResponsiveRow([
            ft.Container(
            col={"xs": 10,"sm": 6, "xl": 4},
            width=.8*page.width,
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
            ],
                                 alignment=ft.MainAxisAlignment.CENTER
                                 ),
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
