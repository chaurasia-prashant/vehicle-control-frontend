import json
import flet as ft
# Using request for getting and sending data to API.
import requests
import secrets

from localStorage.clientStorage import setUserData
from user_controls.urls import urls

# Function for signUP page that return a view.


def Signup(page: ft.page):

    # Fields for registering user to our database
    # Username field
    username = ft.TextField(
        label="Employee Name",
        color=ft.colors.WHITE,
        text_size= 15,
        height= 45,
        expand=True
    )
    # Email field
    email = ft.TextField(
        label="Mail Id",
        color=ft.colors.WHITE,
        text_size= 15,
        height= 45,
        suffix_text= "@tatapower.com",
        expand=True
    )
    # Password Field
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        text_size= 15,
        height= 45,
        expand=True
    )
    confpassword = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        text_size= 15,
        height= 45,
        expand=True
    )
    # employee ID field
    empId = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
        text_size= 15,
        # height= 45,
        expand=True,
        on_blur=lambda e:checkId(e)
    )
    # Department field
    department = ft.TextField(
        label="Department",
        color=ft.colors.WHITE,
        text_size= 15,
        height= 45,
        expand=True
    )
    # phonenumber field
    phoneNumber = ft.TextField(
        label="Phone Number",
        color=ft.colors.WHITE,
        text_size= 15,
        # height= 60,
        expand=True,
        on_change=lambda e:checkPhoneNumber(e)
    )
    inps = "0123456789"
    def checkPhoneNumber(e):
        for val in phoneNumber.value:
            if val not in inps:
                phoneNumber.error_text = "Only numbers allowed"
                phoneNumber.update()
            else:
                phoneNumber.error_text = None
                phoneNumber.update()
        
    def checkId(e):
        try:
            url = urls()
            url =url["allId"]
            response = requests.get(f"{url}")
            result = json.loads(response.content)
            for res in result:
                if empId.value == res["empId"]:
                    empId.error_text = "This id is already in use"
                    empId.update()
                    break
                empId.error_text = None
                empId.update()
        except:
            pass
        
    messageText =ft.Text("Enter credentials to register\n")

    # function that handel registeration process of a user to our database.
    # It communicate with our API through request method.
    def user_registration(e):
        messageText.value = None
        messageText.update()
        # Using try and catch to handle errors.
        try:
            if password.value != confpassword.value:
                messageText.value = "Password not match\n"
                messageText.color = ft.colors.RED_600
                messageText.update()
            elif password.value and username.value and email.value and empId.value and department.value and phoneNumber.value != "":
                page.splash =ft.ProgressBar()
                page.update()    
                data = {
                    "username": username.value.title(),
                    "email": email.value + email.suffix_text,
                    "empId": empId.value,
                    "department": department.value.capitalize(),
                    "phoneNumber": phoneNumber.value,
                    "password": password.value,
                    "isAuthorized": False,
                    "verifyPhoneNumber":False,
                    "verifyEmail":False,
                    "isOwner": False,
                    "isAdmin":False,
                    "uid" : secrets.token_urlsafe(16)
                }
                url =urls()
                url = url["signup"]
                res = requests.post(f"{url}", json=data)
                if res.status_code == 200 and res.text != "404":
                    setUserData(page, data)
                    page.client_storage.set("isAuthenticated", True)
                    page.splash =None
                    page.update()
                    page.go("/home")
                else:
                    page.splash =None
                    page.update()
                    messageText.value = "Something went wrong\n"
                    messageText.color = ft.colors.RED_600
                    messageText.update()
            else:
                messageText.value = "All fields are manedatory\n"
                messageText.color = ft.colors.RED_600
                messageText.update()       
        except:
            page.splash =None
            page.update()
            page.go("/serverNotFound")
    # Signup views for the site.
    SignupPage = ft.View(
        "/signup",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            
            ft.Column(
                [ 
                 ft.Text(" WELCOME",
                    size= 50,
                    color=ft.colors.BLUE_700
                    ),
                    ft.Container(
                        content=ft.ListView(
                            [
                                ft.Container(
                        width=.6*page.width,
                        alignment=ft.alignment.center,
                        content=ft.Container(
                            margin=10,
                            padding=20,
                            bgcolor=ft.colors.BLACK87,
                            border_radius=10,
                            content=ft.ResponsiveRow(
                                [
                                    messageText,
                                    username,
                                    email,
                                    empId,
                                    department,
                                    phoneNumber,
                                    password,
                                    confpassword,
                                   ft.Container(height=10),
                                    ft.Container(
                                        height=45,
                                        # margin=30,
                                        content=ft.Row(
                                            [
                                                ft.ElevatedButton(
                                            "Go Back",
                                            color= ft.colors.BLUE,
                                            bgcolor= ft.colors.WHITE,
                                            on_click=lambda _: page.go("/")
                                        ),
                                                ft.Container(
                                                    width =10),
                                                ft.ElevatedButton(
                                            "Register",
                                            color= ft.colors.WHITE,
                                            bgcolor= ft.colors.BLUE,
                                            expand =True,
                                            on_click=user_registration
                                        )
                                            ],
                                            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
                                        )
                                    ),
                               
                                ]
                            )
                        )


                    ),
                            ]
                        )
                    )
                ],
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # alignment=ft.MainAxisAlignment.CENTER,
                width= .4*page.width,
            )
        ],
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        vertical_alignment= ft.MainAxisAlignment.CENTER
    )

    return SignupPage
