import flet as ft
import requests
# import json to get data return from api
import json

# import for local data storage of user
from localStorage.clientStorage import setUserData

# function for login view


def Login(page: ft.page):

    # empId field for login
    empId = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
        height=50,
    )
    # password field
    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
        height=50,
    )

    # function for handeling user login event.

    def login_user(e):
        data = {
            "empID": empId.value,
            "password": password.value

        }
        page.go("/home")
        print(data)
        try:
            res = requests.post("http://127.0.0.1:8000/", json=data)
            resData = json.loads(res.content)
            setUserData(page, resData)

            if res.status_code == 200:
                print("successfully login")
                page.go("/home")
            else:
                print("you are not a registered user")
        except Exception as e:
            print(e)

    loginPage = ft.View(
        "/",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Column(

                [
                    ft.Text(
                        "Book My Trip",
                        size=40,
                        weight=ft.FontWeight.W_900,
                        color=ft.colors.BLUE_600,

                    ),
                    ft.Container(height=10),
                    ft.ResponsiveRow([
                        ft.Container(
                            content=ft.Image(
                                src=f"/car.png",
                                width=200,
                                height=200,
                                fit=ft.ImageFit.CONTAIN,
                                gapless_playback=True
                            )

                        ),
                        ft.Container(
                            col={"sm": 8, "md": 8, "xl": 6},
                            width=.4*page.width,
                            # alignment=ft.alignment.center,
                            content=ft.Column(
                                [
                                    ft.Container(
                                        margin=10,
                                        padding=15,
                                        bgcolor=ft.colors.BLACK87,
                                        border_radius=10,
                                        content=ft.Column([
                                            ft.Text(
                                                "Enter Credentials to Login",
                                                color=ft.colors.BLUE
                                            ),
                                            empId,
                                            password,

                                        ],
                                        ),
                                    ),

                                    ft.Container(
                                        col={"sm": 8, "md": 8, "xl": 6},
                                        margin=10,
                                        content=ft.Row(
                                            [
                                                ft.Container(
                                                    width=100,
                                                    # If not registered redirect to signup.
                                                    content=ft.ElevatedButton(
                                                        "Signup",
                                                        on_click=lambda _:page.go(
                                                            "/signup")
                                                    ),
                                                    expand=True
                                                ),
                                                ft.Container(
                                                    width=30),
                                                ft.Container(

                                                    width=100,
                                                    # Trigger user login event
                                                    content=ft.ElevatedButton(
                                                        "Login",
                                                        on_click=login_user),
                                                    expand=True
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                        )
                                    )
                                ]
                            )
                        )

                    ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )

                ],
            )
        ]
    )

    return loginPage
