import flet as ft

import requests


def Login(page: ft.page):
    empId = ft.TextField(
        label="Employee ID",
        color=ft.colors.WHITE,
    )

    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        color=ft.colors.WHITE,
    )

    def login_user(e):
        data = {
            "empID": empId.value,
            "password": password.value

        }

        print(data)
        try:
            res = requests.post("http://127.0.0.1:8000/", json=data)
            print(res.text)

            if res.status_code == 200:
                print("successfully login")
                page.go("/home")
            else:
                print("you are not a registered user")
        except:
            print("error")

    loginPage = ft.View(
        "/" ,
        bgcolor= ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Column(

                [
                    ft.Text(
                        "Book My Trip",
                        size=70,
                        weight=ft.FontWeight.W_900,
                        color=ft.colors.BLUE_600,

                    ),

                    ft.Row([

                        ft.Image(
                            src=f"/car.png",
                            width=600,
                            height=600,
                            fit=ft.ImageFit.CONTAIN,
                            gapless_playback=True
                        ),
                        ft.Container(
                            width=.4*page.width,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                [
                                    ft.Container(
                                        margin=30,
                                        padding=30,
                                        bgcolor=ft.colors.BLACK45,
                                        border_radius=10,
                                        content=ft.Column([

                                            empId,
                                            password,

                                        ],
                                        ),
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                margin=30,
                                                width=150,
                                                content=ft.ElevatedButton(
                                                    "Signup",
                                                    on_click=lambda _:page.go(
                                                        "/signup")
                                                )
                                            ),
                                            ft.Container(
                                                margin=30,
                                                width=150,
                                                content=ft.ElevatedButton(
                                                    "Login"),
                                                on_click=login_user
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    )
                                ]
                            )
                        )
                    ])

                ],
            )
        ]
    )

    return loginPage
