from flet import *
from pages.home import Home
from pages.login import Login
from pages.signup import Signup

def views_handler(page,route):

     routes = {
       "/" : Login(page),
       "/home" : Home(page),
       "/signup" : Signup(page)
     }
     
     return routes[route]
        
        
 
 