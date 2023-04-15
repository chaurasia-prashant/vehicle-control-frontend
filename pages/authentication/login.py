import flet as ft
import requests
# import json to get data return from api
import json

# import for local data storage of user
from localStorage.clientStorage import setUserData
from user_controls.urls import urls

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

    mesgText = ft.Text(
        "Enter Credentials to Login",
        color=ft.colors.BLUE
    )

    # function for handeling user login event.

    def login_user(e):
        if empId.value and password.value != "":
            try:
                page.splash = ft.ProgressBar()
                loginBtn.disabled = True
                page.update()
                data = {
                    "empId": empId.value,
                    "password": password.value

                }
                url = urls()
                url = url["login"]
                res = requests.post(f"{url}", json=data)
                resData = json.loads(res.content)
                if res.status_code == 200 and resData[0] == 200:
                    setUserData(page, resData[1])
                    page.client_storage.set("isAuthenticated", True)
                    page.splash = None
                    loginBtn.disabled = False
                    page.go("/home")
                elif resData[0] == 204:
                    mesgText.value = "Incorrect Password"
                    mesgText.color = ft.colors.RED_ACCENT_200
                    page.splash = None
                    loginBtn.disabled = False
                else:
                    mesgText.value = "you are not a registered user"
                    mesgText.color = ft.colors.RED_ACCENT_200
                    page.splash = None
                    loginBtn.disabled = False
            except Exception as e:
                print(e)
                page.splash = None
                loginBtn.disabled = False
                page.go("/serverNotFound")

        else:
            mesgText.value = "All fields are mandatory"
            mesgText.color = ft.colors.RED_ACCENT_200
        page.update()

    loginBtn = ft.ElevatedButton(
        "Login",
        on_click=login_user)
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
                                            mesgText,
                                            empId,
                                            password,
                                            ft.Container(height = 5),
                                            ft.Container(
                                                col={"sm": 8, "md": 8, "xl": 6},
                                                # margin=10,
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
                                                            content=loginBtn,
                                                            expand=True
                                                        ),
                                                    ],
                                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                                )
                                            ),
                                            ft.Container(height = 10),
                                            ft.Row([
                                                ft.Text("  Forget Password?"),
                                                ft.TextButton("Click Here", on_click= lambda _: page.go("/forgotPassword"))
                                            ])

                                        ],
                                        ),
                                    ),



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
