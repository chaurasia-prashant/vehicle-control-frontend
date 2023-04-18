import json
import flet as ft
# Using request for getting and sending data to API.
import requests
import secrets
from database.getFromDb import getRegisteredUser

from localStorage.clientStorage import setUserData
from user_controls.urls import urls

# Function for signUP page that return a view.


def Signup(page: ft.page):
    
    registeredUsers = getRegisteredUser()

    # Fields for registering user to our database
    # Username field
    username = ft.TextField(
        label="Employee Name",
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )
    # Email field
    email = ft.TextField(
        label="Mail Id",
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        suffix_text="@gmail.com",
        expand=True
    )

    # Password Field
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )
    confpassword = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )
    # employee ID field
    empId = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
        text_size=15,
        # height= 45,
        expand=True,
        on_blur=lambda e: checkId(e)
    )
    # Department field
    department = ft.TextField(
        label="Department",
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )
    # phonenumber field
    phoneNumber = ft.TextField(
        label="Phone Number",
        color=ft.colors.WHITE,
        text_size=15,
        # height= 60,
        prefix_text="+91 ",
        expand=True,
        on_blur=lambda e: checkPhoneNumber(e)
    )
    inps = "0123456789"

    def checkPhoneNumber(e):
        phoneNumber.error_text = None
        if len(phoneNumber.value) != 10:
            phoneNumber.error_text = "Phone number not valid"
        for val in phoneNumber.value:
            if val not in inps:
                phoneNumber.error_text = "Only numbers allowed"
        phoneNumber.update()

    def checkId(e):
        try:
            result = registeredUsers
            for res in result:
                if empId.value == res["empId"]:
                    empId.error_text = "This id is already in use"
                    empId.update()
                    break
                empId.error_text = None
                empId.update()
        except:
            pass

    def sendEmailOtp(e):
        loading.visible = True
        loading.update()
        verificationMessage.color = ft.colors.RED_400
        emailValue = email.value + email.suffix_text
        if email.value != "":
            allMails = registeredUsers
            allMails = [mail["email"] for mail in allMails]
            if emailValue in allMails:
                verificationMessage.value = "Email already registered."
                
            else:
                try:   
                    data = {
                        "email": [emailValue]
                    }
                    url = urls()
                    url = url["sendEmailOTP"]
                    res = requests.post(url, json=data)
                    if res.status_code == 200 and res.text == "200":
                        otpField.visible = True
                        getOtp.visible = False
                        validateOtp.visible = True
                        email.disabled = True
                        verificationMessage.value = "Otp sent to your mail ID"
                        verificationMessage.color = ft.colors.GREEN_400
                    else:
                        verificationMessage.value = "Something went wrong! Try again"

                except:
                    verificationMessage.value = "Something went wrong! Try again"
        else:
            verificationMessage.value = "Plese Enter mail id"
        loading.visible = False
        page.update()

    def verifyOtp(e):
        loading.visible = True
        loading.update()
        verificationMessage.color = ft.colors.RED_400
        if email.value != "" and otpField.value != "":
            try:
                emailValue = email.value + email.suffix_text
                data = {
                    "email": emailValue,
                    "otp": otpField.value

                }
                url = urls()
                url = url["verifyEmailOTP"]
                res = requests.post(url, json=data)
                if res.status_code == 200 and res.text == "200":
                    emailVerificationPage.visible = False
                    detailsPage.visible = True

                    verificationMessage.value = "OTP verified successfully"
                    verificationMessage.color = ft.colors.GREEN_400
                elif res.text == "203":
                    verificationMessage.value = "Invalid Otp"
                else:
                    verificationMessage.value = "Something went wrong! Try again"
            except:
                verificationMessage.value = "Something went wrong! Try again"
        else:
            verificationMessage.value = "Plese Enter Otp"
        loading.visible = False
        page.update()

    messageText = ft.Text("Enter credentials to register\n")

    # function that handel registeration process of a user to our database.
    # It communicate with our API through request method.
    def user_registration(e):
        loading.visible = True
        loading.update()
        messageText.value = None
        messageText.update()
        # Using try and catch to handle errors.
        try:
            if password.value != confpassword.value:
                messageText.value = "Password not match\n"
                messageText.color = ft.colors.RED_600
                messageText.update()
            elif password.value and username.value and email.value and empId.value and department.value and phoneNumber.value != "":
                page.splash = ft.ProgressBar()
                page.update()
                data = {
                    "username": username.value.title(),
                    "email": email.value + email.suffix_text,
                    "empId": empId.value,
                    "department": department.value.capitalize(),
                    "phoneNumber": phoneNumber.value,
                    "password": password.value,
                    "isAuthorized": False,
                    "verifyPhoneNumber": False,
                    "verifyEmail": True,
                    "isOwner": False,
                    "isAdmin": False,
                    "uid": secrets.token_urlsafe(16)
                }
                url = urls()
                url = url["signup"]
                res = requests.post(f"{url}", json=data)
                if res.status_code == 200 and res.text != "404":
                    setUserData(page, data)
                    page.client_storage.set("isAuthenticated", True)
                    page.splash = None
                    page.update()
                    page.go("/home")
                else:
                    page.splash = None
                    page.update()
                    messageText.value = "Something went wrong\n"
                    messageText.color = ft.colors.RED_600
                    messageText.update()
            else:
                messageText.value = "All fields are manedatory\n"
                messageText.color = ft.colors.RED_600
                messageText.update()
        except:
            page.splash = None
            page.update()
            page.go("/serverNotFound")
        loading.visible = False
        loading.update()

    # Email verification
    getOtp = ft.ElevatedButton(
        "Get Otp",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        expand=True,
        on_click=sendEmailOtp
    )
    validateOtp = ft.ElevatedButton(
        "Validate OTP",
        visible=False,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        expand=True,
        on_click=verifyOtp
    )

    # Otp field
    otpField = ft.TextField(
        label="OTP",
        visible=False,
        hint_text="Enter otp",
        color=ft.colors.WHITE,
        text_size=15,
        height=50,
        expand=True
    )
    verificationMessage = ft.Text(color=ft.colors.RED_400)

    # Email verification Page
    emailVerificationPage = ft.Container(
        visible=True,
        content=ft.Column(
            [
                ft.ResponsiveRow(
                    controls =[
                        
                        ft.Container(
                            col={"sm": 8, "md": 8, "xl": 6},
                            width=.9*page.width,
                            alignment=ft.alignment.center,
                            margin=10,
                            padding=20,
                            bgcolor=ft.colors.BLACK87,
                            border_radius=10,
                            content=ft.Column([
                                ft.Container(
                                    height=.2*page.height,
                                    content=ft.Column([
                                        ft.Text(
                                    "Enter your mail ID to verify"),
                                email,
                                otpField,
                                verificationMessage,])),
                                ft.Container(height=10),
                                ft.Container(
                                    height=45,
                                    # margin=30,
                                    content=ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Back to login",
                                                color=ft.colors.BLUE,
                                                bgcolor=ft.colors.WHITE,
                                                on_click=lambda _: page.go(
                                                    "/login")
                                            ),
                                            ft.Container(
                                                width=10),
                                            getOtp,
                                            validateOtp
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    )
                                ),
                            ])
                        )

                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )

            ],
            # width=.4*page.width,
        )
    )

    # Details page
    detailsPage = ft.Container(
        # width=.8*page.width,
        visible=False,
        content=ft.Column(
            [
                # ft.Text(" WELCOME",
                #         size=50,
                #         color=ft.colors.BLUE_700
                #         ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(
                            col={"sm": 8, "md": 8, "xl": 6},
                            width=.9*page.width,
                            alignment=ft.alignment.center,
                            margin=10,
                            padding=20,
                            bgcolor=ft.colors.BLACK87,
                            border_radius=10,
                            content=ft.Column([
                                ft.Container(

                                    height=.6*page.height,
                                    content=ft.ListView([
                                        messageText,
                                        username,
                                        # email,
                                        empId,
                                        department,
                                        phoneNumber,
                                        password,
                                        confpassword,
                                    ],

                                        spacing=8)
                                ),
                                ft.Container(height=10),
                                ft.Container(
                                    height=45,
                                    # margin=30,
                                    content=ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Go Back",
                                                color=ft.colors.BLUE,
                                                bgcolor=ft.colors.WHITE,
                                                expand=True,
                                                on_click=lambda _: page.go(
                                                    "/login")
                                            ),
                                            ft.Container(
                                                width=10),
                                            ft.ElevatedButton(
                                                "Register",
                                                color=ft.colors.WHITE,
                                                bgcolor=ft.colors.BLUE,
                                                expand=True,
                                                on_click=user_registration
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        # vertical_alignment= ft.CrossAxisAlignment.END
                                    )
                                ),
                            ])
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )

            ],

        )
    )
    loading = ft.ProgressRing(visible =False,stroke_width=10,bgcolor=ft.colors.PURPLE_600,color=ft.colors.PINK_500)
    
    SignupPage = ft.View(
        "/signup",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Container(
                            alignment=ft.alignment.center,
                            content =ft.Text(" WELCOME",
                        size=35,
                        color=ft.colors.BLUE_700
                        ),
                        ),
            ft.Stack(
                controls=[
                    emailVerificationPage,
                    detailsPage,
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=loading),
                ]
            )


        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )

    return SignupPage
