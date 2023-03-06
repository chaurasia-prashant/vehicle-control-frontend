from flet import *
from user_controls.views import views_handler

def main(page: Page):
  # page.vertical_alignment = MainAxisAlignment.CENTER
  # page.horizontal_alignment = CrossAxisAlignment.CENTER
  page.bgcolor = colors.DEEP_PURPLE_100
  
  
  def route_change(route):
    page.views.clear()
    page.views.append(views_handler(page,page.route))
    page.update()

  def view_pop(view):
    page.views.pop()
    top_view = page.views[-1]
    page.go(top_view.route)
    
  page.on_route_change = route_change
  page.on_view_pop = view_pop
  page.go("/approveRequest")



app(target=main,port =8080, view=WEB_BROWSER, assets_dir="assets")