def urls():
    static = "http://127.0.0.1:8000"
    data = {
        "login": f"{static}/userLogin",
        "signup": f"{static}/userSignup/",
        "allId": f"{static}/allId",
        "vehicleBooking": f"{static}/vehicleBooking/",
        "userBookings": f"{static}/userBookings/",
        "allBookingRequests": f"{static}/allBookingRequests/",
        "approveRequest": f"{static}/approveRequest/",
        "rejectRequest": f"{static}/rejectRequest/",
        "vehicleRegister" : f"{static}/vehicleRegister/",
        "getAllVehicles" : f"{static}/getAllVehicles/",
        
    }
    return data