"""
*********
Rest Framework
*********
"""

# Permission
from tkinter.tix import Tree
from turtle import Turtle
from rest_framework import permissions
from App9SPL.CustomPermission import AllowSuperAdminUser, IsOwnerAndIsSuperAdmin

# Response
from rest_framework.response import Response

# Class - Generic
from rest_framework.generics import GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.views import APIView

# Parser & Status
from rest_framework.parsers import MultiPartParser
from rest_framework import status


# Serializers
from rest_framework.serializers import Serializer

# Error handling
from rest_framework.exceptions import NotFound

# Swagger
from drf_yasg.utils import swagger_auto_schema

# Json Web Token
import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Email for verification
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import get_template

# Forget Password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)

# Search & Filter
from rest_framework.filters import SearchFilter
import django_filters


# Error - Logging
from App9SPL.Error_Log import Error_Log

# JSON Renderer For Encrypt Decrypt
from rest_framework.renderers import JSONRenderer

# Q Object
from django.db.models import Q
from django.db.models import F, Sum, Avg, Count

# Other
from django.http import HttpResponsePermanentRedirect
from django.http import Http404

# Data Time
import datetime

# Json
import json

# Regex
import re


# AuthToken
from App9SPL.AuthToken import DecodeToken


# Models - Admin
from App9SPL.models import (

    # User Models
    SystemUser,

)


# Admin Serializer.
from App9SPL.serializers import (

    # Register Admin User
    register_end_user_serializers,

    # User and Admin Login
    user_login_serializer,

    # Update User PRofile
    update_user_profile_serializers,

    # Get user Serailziers
    Get_User_details_serializers,

    # Log out
    logout_serializers,




)


"""
**************************************************************************
                            Create Your Business Logic here
**************************************************************************
"""


"""
****************************************************************************************************************************************************************
                                                                 End User
****************************************************************************************************************************************************************
"""


"""
********************
    Register End User
********************
"""


class register_end_user_View(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    serializer_class = register_end_user_serializers
    # renderer_classes = (UserRenderer)

    @swagger_auto_schema(tags=["Register User"], operation_description=("End User will create account for using this API. Profile image is optional. use the base64 code to upload profile image. "),)
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(
                data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=False):
                serializer.save()

                return Response({
                    "responseCode": 201,
                    "responseMessage": "Successfully,User is registered.",
                    "responseData": serializer.data, },
                    status=status.HTTP_201_CREATED)
            else:
                if serializer.errors.get('password_length'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Passwords must be bewtween 6  to 25 Characters."},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('username_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Username already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('email_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Email already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Phone Number already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                # Validation
                elif serializer.errors.get('email_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Please, Enter the Correct Email"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('username_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Username must be Alphanumeric & Special Character ('-','.','_')"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('country_code'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Country must be start with '+', and Numeric"},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('Phonedigit'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Phone number must be numeric"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('Phonelength'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'Phone must be bewtween 8  to 12 Characters'},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('first_name_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'First or Last Name must be alphbet.'},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('Last_Name_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'Last Name must be alphbet.'},
                        status=status.HTTP_400_BAD_REQUEST)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": e}, status=status.HTTP_400_BAD_REQUEST)


"""
********************
   Login API 
********************
"""


class user_login_views(GenericAPIView):
    authentication_clesses = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = user_login_serializer

    @swagger_auto_schema(tags=["Register User"], operation_description=("End User and Admin User can login through this API using email and Password "),)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):

            email = request.data["email"]
            GetUserIDLogin = SystemUser.objects.get(email=email).id

            user = SystemUser.objects.get(id=GetUserIDLogin)

            return Response({
                "responseCode": 200,
                "responseMessage": f"Login Successfully. {user.username}",
                "responseData": {"user_Data": user.id,
                                 "user_type": user.user_type,
                                 "image": str(user.profile_images),
                                 "token": {'refresh': user.tokens()['refresh'],
                                           'access': user.tokens()['access']}},
            }, status=status.HTTP_200_OK)

        else:
            if serializer.errors.get("invalid_credentials"):
                return Response({
                    "responseCode": 401,
                    "responseMessage": "Invalid credentials, try again"},
                    status=status.HTTP_401_UNAUTHORIZED)

            elif serializer.errors.get("is_active"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": "Your Account is disable. Please contact Admin"},
                    status=status.HTTP_400_BAD_REQUEST)

            elif serializer.errors.get("delete_account"):
                return Response({
                    "responseCode": 400,
                    "responseMessage": "Your account have been deleted. "},
                    status=status.HTTP_400_BAD_REQUEST)

        return Response({"responseCode": 400, "responseMessage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


"""
********************
   Update User Profile
********************
"""


class update_user_profile_view(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerAndIsSuperAdmin]
    # permission_classes = [AllowSuperAdminUser]

    serializer_class = update_user_profile_serializers

    def get_object(self, pk):
        try:
            return SystemUser.objects.get(pk=pk)
        except SystemUser.DoesNotExist:
            raise NotFound(
                detail={"code": 404, 'message': "Data Not Found"}, code=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=["Register User"], operation_description=("End User can update profile and also admin can update own profile and user profile. "))
    def patch(self, request, pk, format=None):
        try:
            User_ID = self.get_object(pk)

            serializer = self.serializer_class(User_ID, data=request.data,  partial=True,
                                               context={"request": request})

            if serializer.is_valid(raise_exception=False):
                serializer.save()
                user_data = serializer.data

                return Response({
                    "response_code": 200,
                    "response_message": "Admin User profile has been updated.",
                    "response_data": user_data, },
                    status=status.HTTP_200_OK)

            else:

                if serializer.errors.get('username_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Username already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('email_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Email already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('phone_exists'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Phone Number already is existed."},
                        status=status.HTTP_400_BAD_REQUEST)

                # Validation
                elif serializer.errors.get('email_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Please, Enter the Correct Email"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('username_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Username must be Alphanumeric & Special Character ('-','.','_')"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('country_code'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Country must be start with '+', and Numeric"},
                        status=status.HTTP_400_BAD_REQUEST)

                elif serializer.errors.get('Phonedigit'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": "Phone number must be numeric"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('Phonelength'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'Phone must be bewtween 8  to 12 Characters'},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('first_name_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'First or Last Name must be alphbet.'},
                        status=status.HTTP_400_BAD_REQUEST)
                elif serializer.errors.get('Last_Name_validation'):
                    return Response({
                        "responseCode": 400,
                        "responseMessage": 'Last Name must be alphbet.'},
                        status=status.HTTP_400_BAD_REQUEST)

                return Response({"response_code": 400, "response_message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            Error_Log(e)
            return Response({"code": 400, "message": e}, status=status.HTTP_400_BAD_REQUEST)


"""
********************
   Get User Details 
********************
"""


class Get_all_user_details_views(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowSuperAdminUser]
    # permission_classes = [permissions.AllowAny]

    serializer_class = Get_User_details_serializers

    @ swagger_auto_schema(tags=["Get User Details"], operation_description="Get User Details",)
    def get(self, request, format=None):
        user_data = SystemUser.objects.filter(Q(is_active=True))

        if user_data:
            serializer = self.serializer_class(
                user_data, many=True, context={"request": request})

            return Response(
                {"responseCode": 200,
                 'responseMessage': "Success",
                 'responseData': serializer.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {"responseCode": 404,
                 'responseMessage': "No Data", },
                status=status.HTTP_404_NOT_FOUND)


# Log Out
class logout_view(GenericAPIView):
    sauthentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]

    serializer_class = logout_serializers

    @ swagger_auto_schema(tags=["Log in & Log out"], operation_description="Enter the Refresh token for black listing.",)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
