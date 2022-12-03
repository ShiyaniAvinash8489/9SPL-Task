"""
*************************************
        Imported Packages 
*************************************
"""

# Serializer
from dataclasses import field
from email.policy import default
from rest_framework import serializers

# DateTime
from datetime import datetime


# JWT
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Setting.py
from django.conf import settings

# Regular Expression
import re

# Authutication
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Default Util - Forget Password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

# JSON
import json

# Q Object
from django.db.models import Q

# DRF Extra Field
from drf_extra_fields.fields import Base64ImageField


# Admin Models
from App9SPL.models import (
    # Custom User
    SystemUser,


)


"""
****************************************************************************************************************************************************************
                                                                 End User - Serializers
****************************************************************************************************************************************************************
"""


"""
********************
    Register User
********************
"""


class register_end_user_serializers(serializers.ModelSerializer):

    password = serializers.CharField(min_length=6, max_length=50,
                                     write_only=True, required=True, style={"input_type": "password",
                                                                            "placeholder": "Password"},)
    profile_images = Base64ImageField(required=False)

    class Meta:
        model = SystemUser
        fields = ['id',  'first_name', 'last_name', 'username',
                  'country_code', 'phone', 'email', 'password', 'profile_images']

        read_only_fields = ['id', 'user_type']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'country_code': {'required': True},
            'phone': {'required': True},
            'email': {'required': True},
        }

    # Validate Data

    def validate(self, validated_data):

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        country_code = validated_data.get('country_code')
        phone = validated_data.get('phone')
        email = validated_data.get('email')
        password = validated_data.get('password')

        # Exists Data
        username_exists = SystemUser.objects.filter(username=username)
        email_exists = SystemUser.objects.filter(email=email)
        phone_exists = SystemUser.objects.filter(phone=phone)

        if len(password) < 6 or len(password) > 25:
            raise serializers.ValidationError({"password_length":
                                               "Passwords must be bewtween 6  to 25 Characters."})

        # Exists
        elif username_exists:
            raise serializers.ValidationError(
                {"username_exists": "username already is existed."})
        elif email_exists:
            raise serializers.ValidationError(
                {"email_exists": "Email is already existed."})
        elif phone_exists:
            raise serializers.ValidationError(
                {'phone_exists': "Phone Number is already exists."})
        # Validation

        # Email
        elif not re.match('^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$', email):
            raise serializers.ValidationError(
                {'email_validation': "Please, Enter the Correct Email"})

        # Username
        elif not re.match('^[a-zA-Z0-9].[a-zA-Z0-9\.\-_]*[a-zA-Z0-9]$', username):
            raise serializers.ValidationError(
                {"username_validation": "Username must be Alphanumeric & Special Character ('-','.','_')"})

        # Country Code
        elif not re.match('^[+][0-9]*$', country_code):
            raise serializers.ValidationError(
                {"country_code": "Country must be start with '+', and Numeric"})

        # Phone
        # Phone Digit
        elif not phone.isdigit():
            raise serializers.ValidationError(
                {"phone_digit": "Phone number must be numeric"})

        # Phone Length
        elif len(phone) < 8 or len(phone) > 12:
            raise serializers.ValidationError(
                {"phone_length": "Phone must be bewtween 8  to 12 Characters"})

        # First Name
        elif not re.match("^[a-zA-Z]*$", first_name) or not re.match("^[a-zA-Z]*$", last_name):
            raise serializers.ValidationError(
                {"first_name_validation": "First or Last Name must be alphbet."})

        return validated_data

    # Create user
    def create(self, validated_data):
        # if "GST_Img" not in validated_data:
        #     return CourierCompany.objects.create(**decrypt_datas)
        # else:
        return SystemUser.objects.create_user(**validated_data)


"""
********************
    User Login
********************
"""

# Login User with Email


class user_login_serializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=25, min_length=6,
                                     write_only=True)

    class Meta:
        model = SystemUser
        fields = ["email", "password",  "profile_images"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)

        # Raise AuthenticationFailed
        if not user:
            raise serializers.ValidationError(
                {"invalid_credentials": 'Invalid credentials, try again'})
        elif not user.is_active:
            raise serializers.ValidationError(
                {"is_active": 'Your Account is disable. Please contact Admin'})

        elif user.is_blocked == True:
            raise serializers.ValidationError(
                {"delete_account": "Your account have been deleted. "})

        return attrs


"""
********************
    Update Register
********************
"""


class update_user_profile_serializers(serializers.ModelSerializer):

    profile_images = Base64ImageField(required=False, use_url=True)

    class Meta:
        model = SystemUser
        fields = ['id',  'first_name', 'last_name', 'username',
                  'country_code', 'phone', 'email',  'profile_images']

        read_only_fields = ['id', 'user_type']

    # Validate Data

    def validate(self, validated_data):

        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        country_code = validated_data.get('country_code')
        phone = validated_data.get('phone')
        email = validated_data.get('email')

        # Exists Data
        username_exists = SystemUser.objects.filter(username=username)
        email_exists = SystemUser.objects.filter(email=email)
        phone_exists = SystemUser.objects.filter(phone=phone)

        # Exists
        if username_exists:
            raise serializers.ValidationError(
                {"username_exists": "username already is existed."})
        elif email_exists:
            raise serializers.ValidationError(
                {"email_exists": "Email is already existed."})
        elif phone_exists:
            raise serializers.ValidationError(
                {'phone_exists': "Phone Number is already exists."})
        # Validation

        # Email
        if email and not re.match('^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$', email):
            raise serializers.ValidationError(
                {'email_validation': "Please, Enter the Correct Email"})

        # Username
        if username and not re.match('^[a-zA-Z0-9].[a-zA-Z0-9\.\-_]*[a-zA-Z0-9]$', username):
            raise serializers.ValidationError(
                {"username_validation": "Username must be Alphanumeric & Special Character ('-','.','_')"})

        # Country Code
        if country_code and not re.match('^[+][0-9]*$', country_code):
            raise serializers.ValidationError(
                {"country_code": "Country must be start with '+', and Numeric"})

        # Phone
        # Phone Digit
        if phone and not phone.isdigit():
            raise serializers.ValidationError(
                {"phone_digit": "Phone number must be numeric"})

        # Phone Length
        if phone and (len(phone) < 8 or len(phone) > 12):
            raise serializers.ValidationError(
                {"phone_length": "Phone must be bewtween 8  to 12 Characters"})

        # First Name
        if (first_name or last_name) and (not re.match("^[a-zA-Z]*$", first_name) or not re.match("^[a-zA-Z]*$", last_name)):
            raise serializers.ValidationError(
                {"first_name_validation": "First or Last Name must be alphbet."})

        return validated_data


"""
********************
    Get user Details 
********************
"""


class Get_User_details_serializers(serializers.ModelSerializer):

    class Meta:
        model = SystemUser
        fields = '__all__'


"""
********************
    Log Out 
********************
"""

# Log Out


class logout_serializers(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
