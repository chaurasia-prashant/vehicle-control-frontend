import flet as ft
import requests


def Signup(page: ft.page):

    username = ft.TextField(
        label="Employee Name",
        color=ft.colors.WHITE,
        expand=True
    )
    email = ft.TextField(
        label="Mail Id",
        color=ft.colors.WHITE,
        expand=True
    )
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        expand=True
    )
    empID = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
        expand=True
    )
    department = ft.TextField(
        label="Department",
        color=ft.colors.WHITE,
        expand=True
    )
    phoneNumber = ft.TextField(
        label="Phone Number",
        color=ft.colors.WHITE,
        expand=True
    )

    def user_registration(e):
        data = {
            "username": username.value,
            "email": email.value,
            "empID": empID.value,
            "department": department.value,
            "phoneNumber": phoneNumber.value,
            "password": password.value
        }

        try:
            res = requests.post("http://127.0.0.1:8000/user/signup", json=data)
            print(res.text)
            if res.status_code == 200:
                print("successfully login")
                page.go("/login")
            else:
                print("you are not a registered user")
        except:
            print("error")

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
                                        empID,
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
