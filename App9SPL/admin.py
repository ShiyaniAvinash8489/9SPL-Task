"""
*************************************
        Imported Packages
*************************************
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


# Models
from App9SPL.models import (

    # Custom User Model
    SystemUser,

)


"""
**************************************************************************
                                Set Up Admin
**************************************************************************
"""


"""
*************
    User
*************
"""


# User Admin
@admin.register(SystemUser)
class SystemUserAdmin(UserAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'phone', 'is_active', 'user_type']

    # list_filter = ['is_active', 'is_staff', ]

    readonly_fields = ["id", "created_on", "updated_on", ]

    fieldsets = (
        ("Register Info:", {"fields": ("id", "email",
         "username", "country_code", "phone", "password")}),
        ("Personal Info", {
         "fields": ("first_name", "last_name", "profile_images"), },),
        ("User Type", {"fields": ("user_type",), },),

        ("Login Info", {"fields": ("last_login",), },),
        ("Time Stamp Info", {"fields": ("created_on", "updated_on",), },),
        ("Permissions", {"fields": ("user_permissions", "groups"), },),
        ("Admin Login", {"fields": ("is_active", "is_superuser",
         "is_staff",  "is_blocked",), },),
    )
