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
    userData = getUserData(page)

    # Form field need to filled for sending a travel request.
    def checkForGuest(e):
        if isGuestBooking.value:
            guestName.visible = True
            guestPhoneNumber.visible = True
        else:
            guestName.visible = False
            guestPhoneNumber.visible = False
        page.update()

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
    
    isGuestBooking = ft.Checkbox(
        label="Booking For Guest?",
        label_position=ft.LabelPosition.LEFT,
        expand=True,
        on_change=checkForGuest
        )
    
    ishavedepartmentvehicle = False
    if userData["department"] in ["IMD","CMD","CLD"]:
        ishavedepartmentvehicle = True
    isDepartmentVehicle = ft.Checkbox(
        visible= ishavedepartmentvehicle,
        label="Use Department Vehicle?",
        label_position=ft.LabelPosition.LEFT,
        expand=True,
        )
    guestName = ft.TextField(
        visible=False,
        label="Guest name",
        color=ft.colors.WHITE,
        height=50,

    )
    guestPhoneNumber = ft.TextField(
        visible=False,
        label="Guest Phone Number",
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
    
    def validateBookingForm():
        errorText.visible =False
        errorText.update()
        if shour.value == None and sminut.value == None and ehour.value == None and eminut.value == None  :
            errorText.value ="Please enter time"
            errorText.visible =True
            errorText.update()
            return False       
        elif startLocation.value == ""  or destination.value== "" or reasonField.value == "":
            errorText.value ="All fields are manadatory"
            errorText.visible =True
            errorText.update()
            return False   
        
        elif isGuestBooking.value:
            if guestName.value == "" or guestPhoneNumber.value == "":
                errorText.value ="Please enter guest details"
                errorText.visible =True
                errorText.update()
                return False  
            else:
                return True 
        else: return True
    
    def book_request(e):
        
        if validateBookingForm() :
            startTime = int(shour.value)*3600 + int(sminut.value)*60
            endTime = int(ehour.value)*3600 + int(eminut.value)*60
            if endTime > startTime:
                try:
                    vehicleType  = "ADMIN"
                    page.splash =ft.ProgressBar()
                    page.update()
                    if isDepartmentVehicle.value:
                        vehicleType = userData["department"]
                    data = {
                        "bookingNumber": secrets.token_urlsafe(6),
                        "empId": userData["empId"], 
                        "empUsername": userData["username"],
                        "userDepartment": userData["department"],
                        "isGuestBooking": isGuestBooking.value,  #Booking detail added for guest
                        "guestName": guestName.value,  #Booking detail added for guest
                        "guestMobileNumber" : guestPhoneNumber.value,  #Booking detail added for guest
                        "vehicleType": vehicleType,
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
                except Exception as e:
                    print(e)
                    errorText.value = "Something Went Wrong\nUnable to procced your request\n"
                    errorText.visible =True
                    errorText.update()
                    page.splash =None
                    page.update()
            else:
                errorText.value ="End time should be after start time"
                errorText.visible =True
                errorText.update()
            
    bookingForm = ft.ListView(
                            controls =[
                                ft.Container(content=errorText),
                                ft.Container(height=10),
                                ft.Container(content=startLocation),
                                ft.Container(content=destination),
                                ft.Container(content=isDepartmentVehicle),
                                ft.Container(content=isGuestBooking),
                                ft.Container(content=guestName),
                                ft.Container(content=guestPhoneNumber),
                                ft.Container(content=dateDropdown),
                                
                                # startLocation,
                                # destination,
                                # isGuestBooking,
                                # guestName,
                                # guestPhoneNumber,
                                # dateDropdown,
                                ft.Text("  Trip Start Time",color=ft.colors.BLUE),
                                ft.Container(content=startTime),
                                # startTime,
                                ft.Text("  Trip End Time",color=ft.colors.BLUE),
                                ft.Container(content=endTime),
                                ft.Container(content=reasonField),
                                # endTime,
                                # reasonField,
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
                            
                            spacing=10,
                            # expand=1
                        )

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
                        margin=10,
                        padding=20,
                        bgcolor=ft.colors.BLACK87,
                        border_radius=10,
                        content=ft.Container(
                            height = .8*page.height,
                            content=bookingForm,
                        )
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
