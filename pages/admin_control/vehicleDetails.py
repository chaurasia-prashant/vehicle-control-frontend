from datetime import datetime
import json
import time
import flet as ft
import requests
from database.getFromDb import getAllVehicles
from database.staticData import secondsToTime
from localStorage.clientStorage import getUserData
from user_controls.app_bar import Navbar
from user_controls.urls import urls


# vehicles = getAllVehicles()

# Vehicle Detail Page


def VehicleDetail(page: ft.page):
    currentUser = getUserData(page)
    timeText = secondsToTime()

    def closevehicleScreen(e):
        page.client_storage.remove("vehicleBooking")
        dataCol.controls = None
        dataCol.update()

        vehicalBookingScreen.visible = None
        vehicalBookingScreen.visible = False
        vehicalBookingScreen.update()

    def showAddVehicleScreen(e):
        # allVehicleScreen.visible = False,
        # allVehicleScreen.update()
        addVehicleScreen.visible = None
        addVehicleScreen.visible = True
        addVehicleScreen.update()

    def hideAddVehicleScreen(e):
        addVehicleScreen.visible = None
        addVehicleScreen.visible = False
        addVehicleScreen.update()

    # Vehicle card to show vehicles registered.
    def vehicleDetailScreen(vechNumber, vechPhoneNumber, data):
        vehicleDetail = ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Column(
                        [
                            ft.Row([
                                ft.Text(
                                    "Vehicle Number"),
                                ft.Text(
                                    vechNumber,
                                    color=ft.colors.BLUE
                                ),
                            ]),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Text(
                                    "Phone Number"),
                                ft.Text(
                                    vechPhoneNumber
                                ),
                            ]),

                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Container(
                        bgcolor=ft.colors.BLUE_900,
                        border_radius=50,
                        content=ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD_IOS,
                            on_click=lambda e:vehicleBookingTimeLine(e, data)
                        ),
                    )

                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
            )
        )
        return vehicleDetail

    # Card to show vehicle booking history.

    def minBlock(colr, tim):
        minutesBlock = ft.Container(
            padding=7,
            width=60,
            bgcolor=colr,
            content=ft.Text(tim, color=ft.colors.BLACK),

        )
        return minutesBlock

    def mntl(dateTxt, tmline):
        maintimeline = ft.Column([
            ft.Container(height=10),
            ft.Container(content=ft.Text(dateTxt),),
            ft.Container(
                padding=5,
                height=100,
                # width=page.width,
                bgcolor=ft.colors.WHITE,
                border_radius=12,
                content=tmline
            ),

        ])
        return maintimeline

    dataCol = ft.ListView(
        spacing=5,
    )
    
    sideDataCol = ft.ListView(
        spacing=5,
    )

    def vehicleBookingTimeLine(e, data):
        dataCol.controls = None
        dataCol.update()
        sideDataCol.controls = None
        sideDataCol.update()
        if data != None:
            data = json.loads(data)
            keys = list(data.keys())
            keys.sort()
            for i in keys:
                timeline = ft.ListView(
                        spacing=1,
                        horizontal=True,
                    )
                sideTimeline = ft.ListView(
                        spacing=1,
                        horizontal=True,
                    )
                dt =  datetime.strptime(i, "%Y-%m-%d")
                if datetime.now().date() <= dt.date():
                    
                    tims = data[i]
                    dt = []
                    for j in tims.keys():
                        for k in range(int(tims[j][0]), int(tims[j][1]), 1800):
                            dt.append(k)
                    for k in range(0, 86400, 1800):
                        if k in dt:
                            timeline.controls.append(
                                minBlock(colr=ft.colors.RED, tim=timeText[f'{k}']))
                            sideTimeline.controls.append(
                                minBlock(colr=ft.colors.RED, tim=timeText[f'{k}']))
                        else:
                            timeline.controls.append(
                                minBlock(colr=ft.colors.BLUE, tim=timeText[f'{k}']))
                            sideTimeline.controls.append(
                                minBlock(colr=ft.colors.BLUE, tim=timeText[f'{k}']))
                    dataCol.controls.append(mntl(dateTxt=i, tmline=timeline))
                    dataCol.update()
                    sideDataCol.controls.append(mntl(dateTxt=i, tmline=sideTimeline))
                    sideDataCol.update()
            if len(dataCol.controls) == 0:
                dataCol.controls.append(ft.Text("No Booking Found", size=35, color= ft.colors.WHITE))
                dataCol.update()
                sideDataCol.controls.append(ft.Text("No Booking Found", size=35, color= ft.colors.WHITE))
                sideDataCol.update()
        else:
            dataCol.controls.append(ft.Text("No Booking Found", size=35, color= ft.colors.WHITE))
            dataCol.update()
            sideDataCol.controls.append(ft.Text("No Booking Found", size=35, color= ft.colors.WHITE))
            sideDataCol.update()
        if page.width < 576:
            vehicalBookingScreen.visible = None
            vehicalBookingScreen.visible = True
            vehicalBookingScreen.update()  
        # elif dataCol.controls == None:
        #     dataCol.controls.append(ft.Text("No data"))
        #     dataCol.update()
            
            

        #     return dataCol
        # else:
        #     return ft.Text("No data found")

    vehicleNumber = ft.TextField(label="Vehicle Number",border_color=ft.colors.WHITE,focused_border_color=ft.colors.BLUE)
    vehiclePhoneNumber = ft.TextField(label="Phone Number",border_color=ft.colors.WHITE,focused_border_color=ft.colors.BLUE)
    vehicleType = ft.Dropdown(
        label="Select for department vehicle",
        # value= None,
        options=[ft.dropdown.Option("IMD"),
                 ft.dropdown.Option("CMD"),
                 ft.dropdown.Option("EMD"),
                 ft.dropdown.Option("OPN"),
                 ft.dropdown.Option("ADMIN"),
                 ],
        border_color=ft.colors.WHITE,
        focused_border_color=ft.colors.BLUE
    )
    vehicleRegisterMessage = ft.Text(visible=False)

    def addVehicle(e):
        vehicleRegisterMessage.visible = None
        vehicleRegisterMessage.update()
        try:
            url = urls()
            url = url["vehicleRegister"]
            data = {
                "vehicleNumber": vehicleNumber.value,
                "vehicleType" : vehicleType.value,
                "vehiclePhoneNumber": vehiclePhoneNumber.value,
                # "bookedTime" :
            }
            if vehicleType.value != None and vehicleNumber.value and vehiclePhoneNumber.value   != "":
                res = requests.post(f"{url}", json=data)
                if res.status_code == 200 and res.text != "404":
                    vehicleRegisterMessage.value = res.text
                    vehicleRegisterMessage.color = ft.colors.GREEN_600
                    vehicleRegisterMessage.visible = True
                    vehicleRegisterMessage.update()
                    time.sleep(.5)
                    addVehicleScreen.visible = None
                    addVehicleScreen.visible = False
                    addVehicleScreen.update()
                    allVehicleScreen.controls.append(vehicleDetailScreen(
                    vechNumber=data["vehicleNumber"],
                    vechPhoneNumber=data["vehiclePhoneNumber"],
                    data=None
                    ))
                    allVehicleScreen.update()
                else:
                    vehicleRegisterMessage.value = "Something Went Wrong"
                    vehicleRegisterMessage.color = ft.colors.RED_500
                    vehicleRegisterMessage.visible = True
                    vehicleRegisterMessage.update()

            else:
                vehicleRegisterMessage.value = "All fields are mandatory"
                vehicleRegisterMessage.color = ft.colors.RED_500
                vehicleRegisterMessage.visible = True
                vehicleRegisterMessage.update()
        except:
            vehicleRegisterMessage.value = "Something Went Wrong"
            vehicleRegisterMessage.color = ft.colors.RED_500
            vehicleRegisterMessage.visible = True
            vehicleRegisterMessage.update()
        page.update()
            
    # Add a vehicle screen
    addVehicleScreen = ft.Container(
        visible=False,
        # height=.5*page.height,
        # top=100,
        width=.5*page.width,
        # col={"sm": 2, "xl": 3},
        bgcolor=ft.colors.BLACK87,
        padding=15,
        border_radius=10,
        content=ft.Column([
            vehicleRegisterMessage,
            ft.Container(height=10),
            vehicleNumber,
            ft.Container(height=10),
            vehiclePhoneNumber,
            ft.Container(height=10),
            vehicleType,
            ft.Container(height=10),
            ft.Row([
                ft.ElevatedButton(
                    "Close",
                    expand=True,
                    on_click=hideAddVehicleScreen

                ),
                ft.ElevatedButton(
                    "Add Vehicle",
                    expand=True,
                    on_click=addVehicle,

                )
            ]),

        ],
            # alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # vehicle booking's screen that display it's history cards in a list view
    vehicalBookingScreen = ft.Container(
        visible=False,
        height=.8*page.height,
        width=.8*page.width,
        bgcolor=ft.colors.BLACK87,
        padding=15,
        border_radius=10,
        content=ft.Column([
            ft.Container(
                height=.65*page.height,
                col={"xs": 10, "sm": 0, "xl": 0},
                content=dataCol,),
            # ft.Container(height= 15),
            ft.ElevatedButton(
                "Close",
                on_click=closevehicleScreen

            )
        ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )

    # vehicle's screen to display all vehicle registered.
    allVehicleScreen = ft.ListView()
    vehicles = getAllVehicles()
    for vech in vehicles:
        if currentUser["isAdmin"]:
            allVehicleScreen.controls.append(vehicleDetailScreen(
                vechNumber=vech["vehicleNumber"],
                vechPhoneNumber=vech["vehiclePhoneNumber"],
                data=vech["bookedTime"]
                ))
        elif currentUser["isOwner"]:
            if vech["vehicleType"] == currentUser["department"]:
                allVehicleScreen.controls.append(vehicleDetailScreen(
                    vechNumber=vech["vehicleNumber"],
                    vechPhoneNumber=vech["vehiclePhoneNumber"],
                    data=vech["bookedTime"]
                    ))
    vehicleScreeen = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 6, "xl": 3},
                height=page.height,

                content=ft.Column([
                    ft.Row([
                        # ft.ElevatedButton(
                        #     "Show Vehicles", expand=True, on_click=allVehicalList),
                        ft.ElevatedButton(
                            "Add Vehicles", expand=True, on_click=showAddVehicleScreen),
                    ],
                           visible= currentUser["isAdmin"] and not currentUser["isOwner"],
                           ),
                    ft.Container(height=1, width=page.width,
                                 bgcolor=ft.colors.BLACK),
                    ft.Container(
                        height = .95*page.height,
                        content=allVehicleScreen),
                ])
            ),
            ft.Container(
                height=.9*page.height,
                col={"xs": 0, "sm": 6, "xl": 6},
                bgcolor=ft.colors.BLACK87,
                padding=15,
                border_radius=10,
                content=ft.Column([
                    ft.Text("Vehicle Booking Timeline"),
                    ft.Container(
                        height=.8*page.height,
                        content=sideDataCol,),
                ],
                    alignment=ft.MainAxisAlignment.START
                )
            )

        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # main view for to contain all cards and screen.
    vehicleDetail = ft.View(
        "/vehicleDetail",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),

        controls=[
            ft.Stack(
                controls=[
                    vehicleScreeen,
                    vehicalBookingScreen,
                    addVehicleScreen,
                ]
            ),
            
        ]
    )

    return vehicleDetail
