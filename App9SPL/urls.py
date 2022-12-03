"""
*************************************
        Imported Packages 
*************************************
"""


# By Default
from django.contrib import admin
from django.urls import path, include


# Admin APP- Views
from App9SPL.views import (

    # Create Admin User
    register_end_user_View,

    # User Login
    user_login_views,

    # Update User Profile
    update_user_profile_view,

    # Get All User Details
    Get_all_user_details_views,

    # Log out views
    logout_view,

)


"""
**************************************************************************
                            ULRS
**************************************************************************
"""

urlpatterns = [
    # ************************* Admin User *************************

    # Create Admin user
    path("Register_User/", register_end_user_View.as_view(), name="RegisterUser"),

    # User Login
    path("User_Login/", user_login_views.as_view(), name="UserLogin"),

    # Update User Profile
    path("Update-User-Profile/<int:pk>/",
         update_user_profile_view.as_view(), name="UpdateProfile"),

    # Get All User Details
    path("Get-All-User-Details/", Get_all_user_details_views.as_view(),
         name="getalluserdetails"),

    # Log Out
    path('logout/', logout_view.as_view(), name="logout"),
]
