from datetime import datetime
import flet as ft
from database.getFromDb import getUserRequestHistory
from user_controls.app_bar import Navbar

# View to access all request history of a user.
# An Icon in history card to represent a user rquest is approved, pending or canceled.
# Green for accepted.
# Red for rejected.
# Yellow for pending.    

def RequestHistory(page: ft.page):
    
    reqHistory = getUserRequestHistory(page)
    def statusCheck(status,cancled):
            if not cancled:
                if status:
                    return ft.Icon(
                                ft.icons.CHECK_CIRCLE,
                                size=50,
                                color=ft.colors.GREEN,
                            )
                else:
                    return ft.Icon(
                                ft.icons.CHECK_CIRCLE,
                                size=50,
                                color=ft.colors.YELLOW,
                            )
            else:
                return ft.Icon(
                                ft.icons.CHECK_CIRCLE,
                                size=50,
                                color=ft.colors.RED,
                            )
    
    def requestHistoryCard(reqNumber,status,cancled, origin,destination,start,end,date):
        # history card that show how its UI looks like.
        
        historyCard = ft.Card(
            content=ft.Container(

                content=ft.Column(
                    [
                        ft.ListTile(
                            # This Icon represent a user rquest is approved, pending or canceled.
                            # Green for accepted.
                            # Red for rejected.
                            # Yellow for pending.
                            leading=statusCheck(status,cancled),
                            title=ft.Row([
                                ft.Text("Booking ID",
                                        size=13),
                                ft.Text(
                                reqNumber,
                                            size=13)
                                ]),
                            subtitle=ft.ListTile(
                                title=ft.Row([
                                    ft.Text(origin,
                                            size=12),
                                    ft.Text("To",
                                            size=12),
                                    ft.Text(destination,
                                            size=12)
                                ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                subtitle=ft.Row([
                                    ft.Text(start,
                                            size=11),
                                    ft.Text("To",
                                            size=11),
                                    ft.Text(end,
                                            size=11)
                                ],
                                    alignment=ft.MainAxisAlignment.START,
                                )
                            )
                        ),
                        ft.Row(
                            [ft.Text(
                                "Date : ",

                            ),
                                ft.Text(
                                date,

                            ),
                                ft.Container(width=20)
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
        return historyCard
    reqData = ft.ListView()
    if reqHistory != None:
        for res in reqHistory:
            date = datetime.strptime(res["tripDate"], "%Y-%m-%dT%H:%M:%S.%f")
            reqData.controls.append(requestHistoryCard(
                status= res["tripStatus"],
                cancled=res["tripCanceled"],
                reqNumber = res["bookingNumber"], 
                origin = res["startLocation"],
                destination= res["destination"],
                start= res["startTime"],
                end= res["endTime"],
                date= date.date()
                ))
    else:
        reqData.controls.append(ft.Text("No Data Found"))
        

    requestHistory = ft.View(
        "/requestHistory",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),

        controls=[
            ft.ResponsiveRow(
                controls=[
                    
                    ft.Container(
                        col={"sm": 6, "xl": 4},
                        content=reqData,
                    ),

                    ft.Container(
                        col={"xs": 0, "sm": 6, "xl": 6},
                        content=ft.Column([
                            ft.Container(
                                height=120,
                                content=ft.Text(
                                    "Welcome to\nBook My Trip",
                                    size=40,
                                    color=ft.colors.BLUE_800
                                ),
                                alignment=ft.alignment.center,
                            ),

                            ft.Container(
                                height=500,
                                col={"xs": 0, "sm": 4, "xl": 2},
                                content=ft.Image(
                                    f"/car.png",
                                    height=page.height,
                                    width=.5*page.width,
                                    fit=ft.ImageFit.CONTAIN,
                                )
                            )
                        ])
                    )


                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        ]
    )

    return requestHistory
