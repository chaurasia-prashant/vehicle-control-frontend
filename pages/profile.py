import flet as ft

# import for local data storage of user
from localStorage.clientStorage import getUserData, setUserData
from user_controls.app_bar import Navbar
from user_controls.urls import urls

# function for login view


def userProfile(page: ft.page):
    
    user = getUserData(page)
    
    verifyEmail = ft.TextButton("Verify Email", visible= not user["verifyEmail"])
    verifyPhoneNumber = ft.TextButton("Verify PhoneNumber",visible=not user["verifyPhoneNumber"])

    profileView = ft.View(
        "/user/profile",
        appbar=Navbar(page, ft),
        bgcolor=ft.colors.DEEP_PURPLE_100,
        controls=[
            ft.Container(
                width = .5*page.width,
                border_radius=10,
                bgcolor=ft.colors.BLACK,
                padding=20,
                content=ft.Column([
                    ft.Text(user["username"],size=20),
                    ft.Text(user["email"],color=ft.colors.BLUE_400, size=13),
                    ft.Row([
                        ft.Text("Employee ID : "),
                        ft.Text(user["empId"],color=ft.colors.BLUE_400,),
                        
                        ]),
                    ft.Row([
                        ft.Text("Department : "),
                        ft.Text(user["department"].upper(),color=ft.colors.BLUE_400,),
                        
                        ]),
                    ft.Row([
                        ft.Text("Contact Number : "),
                        ft.Text(user["phoneNumber"],color=ft.colors.BLUE_400,),
                        ]),
                    ft.Container(height=50),
                    ft.Row([
                        verifyEmail,
                        verifyPhoneNumber
                        ],
                           alignment= ft.MainAxisAlignment.SPACE_BETWEEN),
                    
                ])
            )
        ],
        # vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER
    )

    return profileView
