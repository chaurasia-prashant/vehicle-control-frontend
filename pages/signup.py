import json
import flet as ft
# Using request for getting and sending data to API.
import requests
import secrets

from localStorage.clientStorage import setUserData

# Function for signUP page that return a view.


def Signup(page: ft.page):

    # Fields for registering user to our database
    # Username field
    username = ft.TextField(
        label="Employee Name",
        color=ft.colors.WHITE,
        expand=True
    )
    # Email field
    email = ft.TextField(
        label="Mail Id",
        color=ft.colors.WHITE,
        expand=True
    )
    # Password Field
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        expand=True
    )
    # employee ID field
    empId = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
        expand=True
    )
    # Department field
    department = ft.TextField(
        label="Department",
        color=ft.colors.WHITE,
        expand=True
    )
    # phonenumber field
    phoneNumber = ft.TextField(
        label="Phone Number",
        color=ft.colors.WHITE,
        expand=True
    )

    # function that handel registeration process of a user to our database.
    # It communicate with our API through request method.
    def user_registration(e):
        data = {
            "username": username.value,
            "email": email.value,
            "empId": empId.value,
            "department": department.value,
            "phoneNumber": phoneNumber.value,
            "password": password.value,
            "uid" : secrets.token_urlsafe(16)
        }
        # Using try and catch to handle errors.
        try:
            res = requests.post("http://127.0.0.1:8000/userSignup/", json=data)
            if res.status_code == 200 and res.text != "404":
                setUserData(page, data)
                page.client_storage.set("isAuthenticated", True)
                page.go("/home")
        except:
            print("error")
    # Signup views for the site.
    SignupPage = ft.View(
        "/signup",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Column(
                [
                    ft.Container(
                        width=.6*page.width,
                        alignment=ft.alignment.center,
                        content=ft.Container(
                            margin=30,
                            padding=30,
                            bgcolor=ft.colors.BLACK45,
                            border_radius=10,
                            content=ft.Column(

                                [

                                    ft.Row([
                                        username,
                                        email,]),
                                    ft.Row([
                                        empId,
                                        department,]),
                                    ft.Row([
                                        phoneNumber,
                                        password]),

                                    ft.Container(
                                        height=50,
                                        margin=30,
                                        width=300,

                                        content=ft.ElevatedButton(
                                            "Login",
                                            on_click=lambda _: page.go("/home")
                                        )
                                    ),
                                ],
                            ),
                        )


                    ),
                    ft.Row([
                        ft.Container(
                            height=50,
                            margin=30,
                            width=300,

                            # Button for sending request for registration event.
                            content=ft.ElevatedButton(
                                "Register",
                                on_click=user_registration
                            )
                        ),
                    ],
                        alignment=ft.MainAxisAlignment.CENTER

                    )



                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )

    return SignupPage
