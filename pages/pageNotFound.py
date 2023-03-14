import flet as ft


def pageNotFound(page):

    errorpage = ft.View(
        "/pageNotFound",
        appbar=ft.AppBar(),
        controls=[
            ft.ResponsiveRow([
                ft.Column(
                    [
                        ft.Text("Page Not Found",
                                size=30),
                        ft.Container(height=20),
                        ft.Container(
                            padding=10,
                            height = .7*page.height,
                            content=ft.Image(
                                src=f"/pagenotfound.png",
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
