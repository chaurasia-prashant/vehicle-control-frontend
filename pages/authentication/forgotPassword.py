import time
import flet as ft
import requests
from user_controls.urls import urls

# Function for signUP page that return a view.


def ForgotPassword(page: ft.page):

    # Reset user password
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
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )

    def sendEmailOtp(e):
        verificationMessage.color = ft.colors.RED_400
        if email.value != "":
            try:
                emailValue = email.value + email.suffix_text
                data = {
                    "email": [emailValue]
                }
                getOtp.disabled = True
                getOtp.update()
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
                    getOtp.disabled = False
                    verificationMessage.value = "Something went wrong! Try again"

            except:
                verificationMessage.value = "Something went wrong! Try again"
        else:
            verificationMessage.value = "Plese Enter mail id"
        page.update()
            
    def verifyOtp(e):
        verificationMessage.color = ft.colors.RED_400
        if email.value != "" and otpField.value != "":
            try:
                emailValue = email.value + email.suffix_text
                data = {
                    "email": emailValue,
                    "otp" : otpField.value
                    
                }
                url = urls()
                url = url["verifyEmailOTP"]
                res = requests.post(url, json=data)
                if res.status_code == 200 and res.text == "200":
                    emailVerificationPage.visible = False
                    ChangePassword.visible = True
                    verificationMessage.value = "OTP verified successfully"
                    verificationMessage.color = ft.colors.GREEN_400
                elif res.text == "203":
                    verificationMessage.value = "Invalid Otp"
                else :
                    verificationMessage.value = "Something went wrong! Try again"
            except:
                verificationMessage.value = "Something went wrong! Try again"
        else:
            verificationMessage.value = "Plese Enter Otp"
        page.update()   
        
    def changePassword(e):
        errorMessage.color = ft.colors.RED_400
        if password.value == confpassword.value:
            if len(password.value) <6:
                errorMessage.value = "Password length must be greater then 6 digit"
            else:
                try:
                    data = {
                        "email": email.value + email.suffix_text,
                        "password" : password.value
                    } 
                    url = urls()
                    url = url["updatePassword"]
                    req = requests.post(url, json = data)
                    if req.status_code == 200 and req.text == "200":
                        errorMessage.value = "Password reset successfully"
                        errorMessage.color = ft.colors.GREEN_400
                        errorMessage.update()
                        time.sleep(.5)
                        page.go("/login")
                except:
                    errorMessage.value = "Something went wrong! Try again"
                
        else:
            errorMessage.value = "Password not match"
        page.update()
            
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
        visible= False,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        expand=True,
        on_click=verifyOtp
    )
    
    # Otp field
    otpField = ft.TextField(
        label="OTP",
        visible= False,
        hint_text= "Enter otp",
        color=ft.colors.WHITE,
        text_size=15,
        height=45,
        expand=True
    )
    submit = ft.ElevatedButton(
        "Submit",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        expand=True,
        on_click=changePassword
    )
    verificationMessage = ft.Text(color= ft.colors.RED_400)
    errorMessage = ft.Text(color= ft.colors.RED_400)
    
    # Email verification Page
    emailVerificationPage = ft.Container(
        visible=True,
        content=ft.Column(
            [
                ft.Text(" Reset Password",
                        size=35,
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
                                            ft.Text("Enter your mail ID to verify"),
                                            email,
                                            otpField,
                                            verificationMessage,

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
                                                        ft.Container(width = 10),
                                                        getOtp,
                                                        validateOtp
                                                    ],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
            width=.4*page.width,
        )
    )
    
    # Change Password
    ChangePassword = ft.Container(
        visible=False,
        content=ft.Column(
            [
                ft.Text(" Reset Password",
                        size=35,
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
                                            ft.Text("Create New Password"),
                                            errorMessage,
                                            password,
                                            confpassword,
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
                                                        ft.Container(width = 10),
                                                        submit,
                                                    ],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
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
            width=.4*page.width,
        )
    )
    
    ForgotPassword = ft.View(
        "/forgotPassword",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Stack(
                controls=[
                    emailVerificationPage,
                    ChangePassword
                ]
            )


        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )

    return ForgotPassword
