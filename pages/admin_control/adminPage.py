import datetime
import json
import time
import flet as ft
import requests
from database.getFromDb import getAllBookkingRequest, getAllVehicles
from database.staticData import secondsToTime
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar
from user_controls.urls import urls

# View for approving a user's travel request
# this page is controlled only by admin
# To approve a request admin have to fill vehicle details and remarks.


def AdminControlPage(page: ft.page):

    def close_banner(e):
        page.banner.open = False
        page.update()

    message = ft.Text(color=ft.colors.BLACK)

    page.banner = ft.Banner(
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED,
                        color=ft.colors.AMBER, size=40),
        content=message,
        actions=[
            ft.TextButton("Close", on_click=close_banner),
        ],
    )

    def show_banner_click(e):
        page.banner.open = True
        page.update()
        time.sleep(2)
        close_banner(e)

    def close_dlg(e):
        getBookingDump.open = False
        assignRoleWindow.visible = False
        page.update()

    moy = ft.Dropdown(
        label="Select Date",
        label_style=ft.TextStyle(size=15),
        height=58,
        text_size=15,
        expand=True
    )
    start_date = datetime.date.today().replace(day=30)
    end_date = datetime.date(2023, 1, 1)

    while start_date >= end_date:
        date_str = start_date.strftime('%m-%Y')
        moy.options.append(ft.dropdown.Option(date_str))
        start_date = start_date - datetime.timedelta(days=31)

    def getBookingDump(e):
        try:
            url = urls()
            requests.post(url["backupBooking"])
            data = {
                "backupDate": moy.value
            }
            res = requests.post(url["getBookingDump"], json=data)
            resdata = json.loads(res.content)
            if res.status_code == 200 and resdata[0] == 200:
                # print(resdata[1])
                close_dlg(e)
            else:
                close_dlg(e)
                message.value = "Something went wrong! Try again."
                message.update()
                show_banner_click(e)

        except Exception as e:
            close_dlg(e)
            message.value = "Something went wrong! Try again."
            message.update()
            show_banner_click(e)

    getBookingDump = ft.AlertDialog(
        modal=True,
        title=ft.Text("Select Month"),
        content=moy,
        actions=[
            ft.TextButton("Cancel", on_click=close_dlg),
            ft.TextButton("Get Backup", on_click=getBookingDump),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_dlg_modal(e):
        page.dialog = getBookingDump
        getBookingDump.open = True
        page.update()

    def validateRoleAssign():
        currentuser = getUserData(page)
        if currentuser["empId"] == userID.value:
            if role.value == "Admin Approver":
                message.value = "Cannot add or remove yourself as admin"
                message.update()
                return False
            elif role.value == "Reject Admin Approver":
                message.value = "Cannot add or remove yourself as admin"
                message.update()
                return False
            elif role.value == None:
                message.value = "Please select action"
                message.update()
                return False
            else:
                return True
        else:
            return True

    def roleAssignHandler(e):
        try:

            if validateRoleAssign():

                selection = {
                    "Department Approver": "assignRole",
                    "Admin Approver": "addAdmin",
                    "Reject Department Approver": "roleReject",
                    "Reject Admin Approver": "removeAdmin",
                }
                data = {
                    "empId": userID.value
                }
                opt = selection[role.value]
                url = urls()
                url = url[opt]
                res = requests.post(f"{url}{userID.value}", json=data)
                if res.status_code == 200 and res.text == "200":
                    data = res.content
                    userID.value = None
                    role.value = None
                    assignRoleWindow.visible = False
                    page.update()
            else:
                show_banner_click(e)

        except Exception as e:
            print(e)

    userID = ft.TextField(
        label="Enter Employee ID",
        color=ft.colors.WHITE,
        height=50,
    )

    role = ft.Dropdown(
        label="Select Action",
        color=ft.colors.WHITE,
        options=[ft.dropdown.Option("Department Approver"),
                 ft.dropdown.Option("Admin Approver"),
                 ft.dropdown.Option("Reject Department Approver"),
                 ft.dropdown.Option("Reject Admin Approver"),
                 ]
    )

    assignRoleWindow = ft.Container(
        visible=False,
        width=4*page.width,
        bgcolor=ft.colors.BLUE_GREY_400,
        border_radius=15,
        padding=15,
        content=ft.Column([
            userID,
            role,
            ft.ElevatedButton(
                "Done",
                on_click=roleAssignHandler
            ),

        ])
    )

    def assignRoleVisible(e):
        assignRoleWindow.visible = True
        assignRoleWindow.update()

    def controlbadges(txt, color, goto):
        badge = ft.Container(
            width=.4*page.width,
            content=ft.ElevatedButton(
                txt,
                bgcolor=color,
                height=50,
                on_click=lambda _: page.go(goto),
                color=ft.colors.WHITE,

            )
        )

        return badge

    mainScreen = ft.ResponsiveRow([
        ft.Container(
            margin=20,
            padding=10,
            col={"sm": 6, "xl": 4},
            height=.9*page.height,
            content=ft.ListView([
                controlbadges(
                    "Approve User Booking Request",
                    ft.colors.BLUE_300,
                    "/approveRequest"
                ),
                # ft.Container(height=20),
                controlbadges(
                    "Get Vehicle Booking Status",
                    ft.colors.DEEP_PURPLE_300,
                    "/vehicleDetail"
                ),

                # ft.Container(height=20),
                ft.Container(
                    width=.4*page.width,
                    content=ft.ElevatedButton(
                        "Assign Role",
                        bgcolor=ft.colors.PURPLE_300,
                        height=50,
                        on_click=assignRoleVisible,
                        color=ft.colors.WHITE,

                    )
                ),
                # ft.Container(height=20),
                ft.Container(
                    width=.4*page.width,
                    content=ft.ElevatedButton(
                        "Get Booking History",
                        bgcolor=ft.colors.PURPLE_300,
                        height=50,
                        on_click=open_dlg_modal,
                        color=ft.colors.WHITE,

                    )
                ),
                ft.Container(content=assignRoleWindow),


            ],
                spacing=20)
        ),
        ft.Container(
            # height=500,
            col={"xs": 0, "sm": 5, "xl": 4},
            margin=30,
            content=ft.Image(
                f"/approve.png",
                height=page.height,
                width=.5*page.width,
                fit=ft.ImageFit.CONTAIN,
            ),
            alignment=ft.alignment.center
        )
    ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    adminControl = ft.View(
        "/adminControlPage",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),
        controls=[
            ft.Stack(
                controls=[
                    mainScreen
                ]
            )
        ]
    )

    return adminControl
