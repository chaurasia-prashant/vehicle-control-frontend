import flet as ft


def serverError(page):

    errorpage = ft.View(
        "/serverNotFound",
        appbar=ft.AppBar(),
        controls=[
            ft.ResponsiveRow([
                ft.Column(
                    [
                        ft.Text("Server Error",
                                size=30),
                        ft.Container(height=20),
                        ft.Container(
                            padding=10,
                            height = .7*page.height,
                            content=ft.Image(
                                src=f"/servernotfound.png",
                                fit=ft.ImageFit.CONTAIN
                            )
                        ),
                        ft.Container(height=30),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),

            ],
                
                
            )
        ],
        
    )

    return errorpage
