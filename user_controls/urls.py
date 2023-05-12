
def urls():
    static = "http://127.0.0.1:8000/api/mpl_VM"
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
        "sendEmailOTP"  : f"{static}/sendEmailOTP/",
        "verifyEmailOTP"  : f"{static}/verifyEmailOTP/",
        "updatePassword" : f"{static}/updatePassword/",
        "backupBooking" : f"{static}/backupBooking/",
        "getBookingDump" : f"{static}/getBookingDump/",
        "assignRole" : f"{static}/assignRole/",
        "roleReject" : f"{static}/roleReject/",
        "addAdmin" : f"{static}/addAdmin/",
        "removeAdmin" : f"{static}/removeAdmin/",
    }
    return data