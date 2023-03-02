import flet as ft


def Home(page: ft.page):
    
    homePage = ft.View(
        "/home",
        controls=[

            ft.Stack(
                [
                    ft.Column(

                        [
                            ft.Text(
                                "Book My Trip",
                                size=70,
                                weight=ft.FontWeight.W_900,
                                color=ft.colors.BLUE_600,

                            ),

                            ft.Image(
                                src=f"/car.png",
                                width=500,
                                height=500,
                                fit=ft.ImageFit.CONTAIN,
                                gapless_playback= True
                            ),

                            ft.ElevatedButton(
                                "Get Start",
                                on_click=lambda _: page.go("/")
                            )

                        ]
                    )
                ]
            )
        ]
    )

    return homePage
