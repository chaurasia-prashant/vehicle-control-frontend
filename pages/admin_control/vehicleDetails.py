import json
import time
import flet as ft
import requests
from database.getFromDb import getAllVehicles
from database.staticData import secondsToTime
from user_controls.app_bar import Navbar
from user_controls.urls import urls



# vehicles = getAllVehicles()

# Vehicle Detail Page


def VehicleDetail(page: ft.page):
    timeText = secondsToTime()
    # if curreVehicleData != None:
    #     curreVehicleData = json.loads(curreVehicleData)
    # else:
    #     curreVehicleData = None

    # Function to show status and booking's of a vehicle
    def showvehicleScreen(e,data):
        page.client_storage.set("vehicleBooking", data)
        if page.width < 576:
            vehicalBookingScreen.visible = None
            vehicalBookingScreen.visible = True
            vehicalBookingScreen.update()
        page.update()

    # hide vehicle booking history
    def closevehicleScreen(e):
        # print("befor remove")
        # print(page.client_storage.get("vehicleBooking"))
        page.client_storage.remove("vehicleBooking")
        # print("after remove")
        # print(page.client_storage.get("vehicleBooking"))
        dataCol.controls = None
        dataCol.update()
        
        vehicalBookingScreen.visible = None
        vehicalBookingScreen.visible = False
        vehicalBookingScreen.update()
        
    def showAddVehicleScreen(e):
        addVehicleScreen.visible = None
        addVehicleScreen.visible = True
        addVehicleScreen.update()
        
    def hideAddVehicleScreen(e):
        addVehicleScreen.visible = None
        addVehicleScreen.visible = False
        addVehicleScreen.update()
        

    # Vehicle card to show vehicles registered.
    def vehicleDetailScreen(vechNumber,vechPhoneNumber,data):
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
                            on_click= lambda e:vehicleBookingTimeLine(e, data)
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
    
    def minBlock(colr,tim):
        minutesBlock = ft.Container(
            padding=7,
            width=60,
            bgcolor=colr,
            content= ft.Text(tim,color=ft.colors.BLACK),
            
            ) 
        return minutesBlock
    

    def mntl(dateTxt,tmline):
        maintimeline = ft.Column([
            ft.Container(height=10),
            ft.Container(content=ft.Text(dateTxt),),
            ft.Container(
                padding = 5,
                height=100,
                width=page.width,
                bgcolor=ft.colors.WHITE,
                border_radius=12,
                content=tmline
                ),
            
            ])
        return maintimeline   
     
    dataCol = ft.ListView(
        spacing=5,
        )
    def vehicleBookingTimeLine(e,data):
        # print("update")
        # print(data)
        if page.width < 576:
            vehicalBookingScreen.visible = None
            vehicalBookingScreen.visible = True
            vehicalBookingScreen.update()
        
        # print(data)
        if data != None:
            data = json.loads(data)
            # data  = sorted(data)
            keys = list(data.keys())
            keys.sort() 
            for i in keys:
                timeline = ft.ListView(
                spacing=1,
                horizontal= True,
                )
                tims = data[i]
                dt = []
                for j in tims.keys():
                    for k in range(int(tims[j][0]),int(tims[j][1]),1800):
                        dt.append(k)
                for k in range(0,86400,1800):
                    if k in dt:
                        timeline.controls.append(minBlock(colr = ft.colors.RED,tim = timeText[f'{k}']))
                    else:
                        timeline.controls.append(minBlock(colr = ft.colors.BLUE,tim = timeText[f'{k}']))
                dataCol.controls.append(mntl(dateTxt=i,tmline=timeline))
                dataCol.update()
        #     return dataCol
        # else:
        #     return ft.Text("No data found")
    
    # vehicleBookHistory = ft.Container(
    #     bgcolor=ft.colors.PURPLE_900,
    #     border_radius=10,
    #     content=ft.Column(
    #         [
    #             ft.Container(
    #                 content=ft.Row([
    #                     ft.Text(
    #                         "Date :",
    #                         weight=ft.FontWeight.BOLD),
    #                     ft.Text(
    #                         "DD-MM-YYYY",
    #                         weight=ft.FontWeight.BOLD
    #                     ),
    #                 ]),
    #             ),

    #             ft.Container(height=4),
    #             ft.Text(
    #                 "Prashant Kumar Chaurasia"
    #             ),
    #             ft.Container(height=2),
    #             ft.Row([
    #                 ft.Text(
    #                     "Department :"),
    #                 ft.Text(
    #                     "IMD"
    #                 ),
    #             ]),
    #             ft.Container(height=2),
    #             ft.Row([
    #                 ft.Text(
    #                     "3:50"),
    #                 ft.Text(
    #                     "To"
    #                 ),
    #                 ft.Text(
    #                     "5:50"
    #                 ),
    #             ]),

    #         ],
    #         alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    #     ),
    #     padding=20,
    # )
    
    vehicleNumber = ft.TextField(label= "Vehicle Number")
    vehiclePhoneNumber = ft.TextField(label= "Phone Number")
    vehicleRegisterMessage = ft.Text(visible=False)
    
    def addVehicle(e):
        vehicleRegisterMessage.visible = None
        vehicleRegisterMessage.update()
        try:
            url = urls()
            url = url["vehicleRegister"]
            data = {
                "vehicleNumber" : vehicleNumber.value,
                "vehiclePhoneNumber" : vehiclePhoneNumber.value,
                # "bookedTime" : 
            }
            if vehicleNumber.value and vehiclePhoneNumber.value != "":
                res = requests.post(f"{url}", json =data)
                if res.status_code == 200 and res.text != "404":
                    vehicleRegisterMessage.value = res.text
                    vehicleRegisterMessage.color =ft.colors.GREEN_600
                    vehicleRegisterMessage.visible = True
                    vehicleRegisterMessage.update()
                    time.sleep(.5)
                    addVehicleScreen.visible = None
                    addVehicleScreen.visible = False
                    addVehicleScreen.update()
                else:
                    vehicleRegisterMessage.value = "Something Went Wrong"
                    vehicleRegisterMessage.color =ft.colors.RED_500
                    vehicleRegisterMessage.visible = True
                    vehicleRegisterMessage.update()
                    
            else:
                vehicleRegisterMessage.value = "All fields are mandatory"
                vehicleRegisterMessage.color =ft.colors.RED_500
                vehicleRegisterMessage.visible = True
                vehicleRegisterMessage.update()
        except:
            vehicleRegisterMessage.value = "Something Went Wrong"
            vehicleRegisterMessage.color =ft.colors.RED_500
            vehicleRegisterMessage.visible = True
            vehicleRegisterMessage.update()
            
    # Add a vehicle screen
    addVehicleScreen = ft.Container(
        visible=False,
        # height=.5*page.height,
        width=.8*page.width,
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
            ft.Row([
                ft.ElevatedButton(
                "Close",
                expand =True,
                on_click=hideAddVehicleScreen

            ),
                ft.ElevatedButton(
                "Add Vehicle",
                expand =True,
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
    def allVehicalList(e):
        vehicles = getAllVehicles()
        for vech in vehicles:
            allVehicleScreen.controls.append(vehicleDetailScreen(
                vechNumber= vech["vehicleNumber"],
                vechPhoneNumber=  vech["vehiclePhoneNumber"],
                data= vech["bookedTime"]
            )) 
        page.update()
    
    
    vehicleScreeen = ft.ResponsiveRow(
        controls=[
            ft.Container(
                col={"sm": 6, "xl": 3},
                height=page.height,
                
                content=ft.Column([
                    ft.Row([
                        ft.ElevatedButton("Show Vehicles",expand=True, on_click=allVehicalList),
                        ft.ElevatedButton("Add Vehicles",expand=True, on_click= showAddVehicleScreen),
                        ]),
                    ft.Container(height=1, width=page.width, bgcolor= ft.colors.BLACK),
                    allVehicleScreen,
                ])
            ),

            ft.Container(
                margin=30,
                col={"xs": 0, "sm": 5, "xl": 4},
                content=ft.Column([
                    ft.Container(
                        height=120,
                        content=ft.Text(
                            "Vehicle Booking History",
                            size=40,
                            color=ft.colors.BLUE_800
                        ),
                        alignment=ft.alignment.center,
                    ),

                    ft.Container(
                        height=500,
                        col={"xs": 0, "sm": 4, "xl": 2},
                        content=ft.ListView(
                            controls=[dataCol,]
                        )
                    )
                ])
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
            )
        ]
    )

    return vehicleDetail
