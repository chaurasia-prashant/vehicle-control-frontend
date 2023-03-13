from datetime import datetime, date
from json import dumps
import secrets
import time
import flet as ft
import requests
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar

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
    startTime = ft.TextField(
        label="Start Time",
        color=ft.colors.WHITE,
        height=50,

    )
    endTime = ft.TextField(
        label="End Time",
        color=ft.colors.WHITE,
        height=50,

    )
    
    errorText = ft.Text("All fields are menedatory",
                        size=14,
                        color= ft.colors.RED_400,
                        visible=False)
    
    
    def book_request(e):
        userData = getUserData(page)
        data = {
            "bookingNumber": secrets.token_urlsafe(6),
            "empId": userData["empId"], 
            "empUsername": userData["username"],
            "userDepartment": userData["department"],
            "tripDate": str(datetime.now()),
            "startLocation": startLocation.value,
            "destination": destination.value,
            "startTime": startTime.value,
            "endTime": endTime.value,
            "vehicleAlloted": None,
            "vehicleNumber": None,
            "tripStatus": False,
            "tripCompleted": False,
            "tripCanceled": False,
            "reason": None,
            "remark": None,
        }
        # Using try and catch to handle errors.
        if startLocation.value  and destination.value and startTime.value and endTime.value != "":
            try:
                
                res = requests.post("http://127.0.0.1:8000/vehicleBooking/", json=data)
                if res.status_code == 200 and res.text != "404":
                    errorText.value = "Request Send Successfuly"
                    errorText.color = ft.colors.GREEN_400
                    errorText.visible =True
                    errorText.update()
                    time.sleep(1)
                    page.go("/home")
            except:
                errorText.value = "Something Went Wrong\nUnable to procced your request\n"
                errorText.visible =True
                errorText.update()
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
                        width=.4*page.width,
                        col={"sm": 6, "xl": 6},
                        margin=30,
                        padding=30,
                        bgcolor=ft.colors.BLACK87,
                        border_radius=10,
                        content=ft.Column(

                            [
                                errorText,
                                startLocation,
                                destination,
                                startTime,
                                endTime,
                                ft.Container(height=30),
                                ft.ElevatedButton(
                                    "Send Travel Request",
                                    # height= 20,
                                    width=.4*page.width - 30,
                                    bgcolor=ft.colors.WHITE,
                                    color=ft.colors.BLUE,
                                    on_click=book_request,
                                    
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
