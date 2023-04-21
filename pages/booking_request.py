from datetime import datetime, date,timedelta
from json import dumps
import secrets
import time
import flet as ft
import requests
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar
from user_controls.urls import urls

# Booking request view
# from this page a user can send a travel request to admin


def BookingRequest(page: ft.page):

    # Form field need to filled for sending a travel request.

    startLocation = ft.TextField(
        label="Start Location",
        color=ft.colors.WHITE,
        height=50,

    )
    destination = ft.TextField(
        label="Destination",
        color=ft.colors.WHITE,
        height=50,

    )
    dateField = ft.Dropdown(
            label="Trip Date",
            label_style= ft.TextStyle(size=15),
            height=58,
            text_size= 15,
            expand= True
        )
    dateDropdown = ft.Container(
        content= ft.Row([
            dateField
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )
    shour = ft.Dropdown(
            label="Hour",
            label_style= ft.TextStyle(size=15),
            height=58,
            text_size= 15,
            expand= True
        )
    sminut = ft.Dropdown(
            label="Minute",
            label_style= ft.TextStyle(size=15),
            height=58,
            text_size= 15,
            expand= True
        )
    startTime = ft.Row([
        shour,
        ft.Text(":"),
        sminut
    ])
    ehour = ft.Dropdown(
            label="Hour",
            label_style= ft.TextStyle(size=15),
            height=58,
            text_size= 15,
            expand= True
        )
    eminut = ft.Dropdown(
            label="Minute",
            label_style= ft.TextStyle(size=15),
            height=58,
            text_size= 15,
            expand= True
        )
    endTime = ft.Row([
        ehour,
        ft.Text(":"),
        eminut
    ])
    
    reasonField = ft.TextField(
        label="Remark",
        hint_text="Trip detail",
        color=ft.colors.WHITE,
        height=50,

    )

    
    errorText = ft.Text("All fields are menedatory",
                        size=14,
                        color= ft.colors.RED_400,
                        visible=False)
    
    nw = datetime.today()
    for i in range(7):
        tm = nw + timedelta(days=i)
        dateField.options.append(ft.dropdown.Option(tm.date()))
    for i in range(24):
        shour.options.append(ft.dropdown.Option(i))
        ehour.options.append(ft.dropdown.Option(i))
    for i in ["00", "30"]:
        sminut.options.append(ft.dropdown.Option(i))
        eminut.options.append(ft.dropdown.Option(i))
        

    
    def book_request(e):
        errorText.visible =False
        errorText.update()
        # Using try and catch to handle errors.
        
        if shour.value == None and sminut.value == None and ehour.value == None and eminut.value == None  :
            errorText.value ="Please enter time"
            errorText.visible =True
            errorText.update()
        elif startLocation.value  and destination.value and reasonField.value != "":
            try:
                page.splash =ft.ProgressBar()
                page.update()
                userData = getUserData(page)
                startTime = int(shour.value)*3600 + int(sminut.value)*60
                endTime = int(ehour.value)*3600 + int(eminut.value)*60
                data = {
                    "bookingNumber": secrets.token_urlsafe(6),
                    "empId": userData["empId"], 
                    "empUsername": userData["username"],
                    "userDepartment": userData["department"],
                    "tripDate": dateField.value,
                    "startLocation": startLocation.value,
                    "destination": destination.value,
                    "startTime": startTime,
                    "endTime": endTime,
                    "vehicleAlloted": None,
                    "vehicleNumber": None,
                    "tripStatus": False,
                    "tripCompleted": False,
                    "tripCanceled": False,
                    "reason": reasonField.value,
                    "remark": None,
                }
                url =urls()
                url =url["vehicleBooking"]
                res = requests.post(f"{url}", json=data)
                if res.status_code == 200 and res.text != "404":
                    errorText.value = "Request Send Successfuly"
                    errorText.color = ft.colors.GREEN_400
                    errorText.visible =True
                    errorText.update()
                    time.sleep(1)
                    page.splash =None
                    page.update()
                    page.go("/home")
            except:
                errorText.value = "Something Went Wrong\nUnable to procced your request\n"
                errorText.visible =True
                errorText.update()
                page.splash =None
                page.update()
        else:
            errorText.visible =True
            errorText.update()
            

    bookingRequest = ft.View(
        "/bookingRequest",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        controls=[
            ft.ResponsiveRow(
                controls=[
                        ft.Container(
                        # width=.4*page.width,
                        col={"sm": 6, "xl": 6},
                        margin=30,
                        padding=30,
                        # height = .8*page.height,
                        bgcolor=ft.colors.BLACK87,
                        border_radius=10,
                        content=ft.Column(
                            controls =[
                                errorText,
                                startLocation,
                                destination,
                                dateDropdown,
                                
                                ft.Text("  Trip Start Time",color=ft.colors.BLUE),
                                startTime,
                                ft.Text("  Trip End Time",color=ft.colors.BLUE),
                                endTime,
                                reasonField,
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "Send Travel Request",
                                    # expand =True,
                                    col={"xs": 8,"sm": 6, "xl": 6},
                                    width=.8*page.width - 30,
                                    bgcolor=ft.colors.WHITE,
                                    color=ft.colors.BLUE,
                                    on_click=book_request,
                                    
                                ),
                            ],
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
                                    f"/request.png",
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
