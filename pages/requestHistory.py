from datetime import datetime
import flet as ft
from database.getFromDb import getUserRequestHistory
from database.staticData import secondsToTime
from user_controls.app_bar import Navbar

# View to access all request history of a user.
# An Icon in history card to represent a user rquest is approved, pending or canceled.
# Green for accepted.
# Red for rejected.
# Yellow for pending.


def RequestHistory(page: ft.page):

    reqHistory = getUserRequestHistory(page)
    timeTxt = secondsToTime()

    def statusCheck(status, cancled):
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

    def closeDialoge(e):
        dlg_modal.open = False
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Trip Status", size=15, color=ft.colors.BLUE_300),
        actions=[
            ft.TextButton("Close", on_click=closeDialoge),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        # on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def openDialoge(e, vehicle, vehicleNo, remark, status, canceled):
        if canceled:
            dlg_modal.content = ft.Container(
                content=ft.ResponsiveRow([
                    ft.Text(
                        f"Your request has been canceled!"),
                    ft.Text(f"Remark : {remark}")
                ])
            )
        else:
            if status:
                dlg_modal.content = ft.Container(
                    content=ft.ResponsiveRow([
                        ft.Text(f"Vehicle No : {vehicle}"),
                        ft.Text(f"Vehicle Phone No : {vehicleNo}"),
                        ft.Text(f"Remark : {remark}")
                    ])
                )
            else:
                dlg_modal.content = ft.Text("Pending For confirmation")
        # dlg_modal.content = details
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def requestHistoryCard(reqNumber, status, cancled, origin, destination, start, end, date, vehicleAllot, vehicleNo, remark):
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
                            leading=statusCheck(status, cancled),
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
                            [
                                ft.TextButton("Details", on_click=lambda e:openDialoge(
                                    e, vehicleAllot, vehicleNo, remark, status, cancled)),

                                ft.Text(
                                    f"Date : {date}"

                                ),
                                ft.Container(width=20)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
        return historyCard
    canceledData = ft.ListView()
    pendingData = ft.ListView()
    approvedData = ft.ListView()

    if reqHistory != [] and reqHistory != None:
        for res in reqHistory:
            # date = datetime.strptime(res["tripDate"], "%Y-%m-%dT%H:%M:%S.%f")
            startTime = res["startTime"]
            endTime = res["endTime"]
            cardValue = requestHistoryCard(
                status=res["tripStatus"],
                cancled=res["tripCanceled"],
                reqNumber=res["bookingNumber"],
                origin=res["startLocation"],
                destination=res["destination"],
                start=timeTxt[startTime],
                end=timeTxt[endTime],
                date=res["tripDate"],
                vehicleAllot=res["vehicleAlloted"],
                vehicleNo=res["vehicleNumber"],
                remark=res["remark"],
            )
            if res["tripCanceled"]:
                canceledData.controls.append(cardValue)
            else:
                if res["tripStatus"]:
                    approvedData.controls.append(cardValue)
                elif not res["tripStatus"] :
                    pendingData.controls.append(cardValue)
    else:
        canceledData,pendingData,approvedData = ft.Container(padding=30, content=ft.Text("No Requests Created",
                                                           size=50,
                                                           color=ft.colors.BLACK))

    requestHistory = ft.View(
        "/requestHistory",
        bgcolor=ft.colors.DEEP_PURPLE_100,
        appbar=Navbar(page, ft),

        controls=[
            ft.ResponsiveRow(
                controls=[

                    ft.Container(
                        col={"sm": 6, "xl": 4},
                        height=.9*page.height,
                        bgcolor=ft.colors.BLACK45,
                        border_radius=10,
                        padding =5,
                        content=ft.Tabs(
                            selected_index=0,
                            animation_duration=300,
                            tabs =[
                                ft.Tab(
                                    text = "Pending",
                                    content= ft.Container(
                                        height= .89*page.height,
                                        content=pendingData,
                                    )
                                ),
                                ft.Tab(
                                    text = "Approved",
                                    content= ft.Container(
                                        height= .89*page.height,
                                        content=approvedData,
                                    )
                                ),
                                ft.Tab(
                                    text = "Rejected",
                                    content= ft.Container(
                                        height= .89*page.height,
                                        content=canceledData,
                                    )
                                )
                            ],
                            
                        )
                    ),

                    ft.Container(
                        col={"xs": 0, "sm": 6, "xl": 6},
                        content=ft.Column([
                            ft.Container(
                                height=120,
                                content=ft.Text(
                                    "My Request\nHistory",
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
