"""
*************************************
        Imported Packages
*************************************
"""

# By Default
from enum import unique
from django.db import models

# Custom User
from django.contrib.auth.models import AbstractUser, AnonymousUser

# Import UserManager Model
from App9SPL.UserManager import UserManager

# JWT
from rest_framework_simplejwt.tokens import RefreshToken


"""
**************************************************************************
                            Create Your models here
**************************************************************************
"""


"""
*************************************
        Custom User Models
*************************************
"""


# Custom User
class SystemUser(AbstractUser):

    # Personal Details and Address , Username, Password
    first_name = models.CharField(max_length=150, null=True,
                                  blank=True)
    last_name = models.CharField(max_length=150, null=True,
                                 blank=True)
    username = models.CharField(max_length=50, unique=True, null=True,
                                blank=True)

    country_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)

    email = models.EmailField(max_length=254, unique=True,
                              null=True, blank=True)

    password = models.CharField(max_length=100, null=True, blank=True)

    # User Type
    user_type = models.CharField(max_length=50, choices=[("EndUser", "EndUser"), ("Admin", "Admin"),],
                                 default="EndUser")
    # Images
    profile_images = models.ImageField(
        upload_to='user_profile', null=True, blank=True, max_length=100)

    # Verify Account
    is_active = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    # Admin
    is_staff = models.BooleanField(default=False)

    # Imp Fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # Username & Required Fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["phone", 'username']

    # Import Module of UserMagers.py
    objects = UserManager()

    def __unicode__(self):
        return self.id

    def __str__(self):
        name = (f"{self.username} {self.phone}")
        return (name)
        # return f'{self.review_category} ({self.review_question})'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
