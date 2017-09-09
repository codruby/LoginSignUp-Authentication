from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from random import randint
from .models import AppUser
import time
import requests
from mailer import mail
from datetime import datetime
from AuthUtil import AuthUtil
from functools import wraps
from django.contrib.auth.hashers import make_password
import re

# JWT Imports
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def jwt_decorator(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        # print request.META
        if request.META.get('HTTP_AUTHORIZATION'):
            token = request.META.get('HTTP_AUTHORIZATION')
            token = AuthUtil.getTokenContent(token.split(' ')[1])
            if token:
                user = authenticate(email=token["user"]["email"], password=token["user"]["password"])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return func(request, *args, token=token["user"])
                else:
                    return Response({"message": "Token Invalid, Redirect to Login"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Token Expired, Redirect to Login"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Invalid Request Token"}, status=status.HTTP_400_BAD_REQUEST)

    return inner


@api_view(['POST'])
def signup_user(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user_details = AppUser.objects.create_user(email=form.cleaned_data["email"],
                                                   first_name=form.cleaned_data["first_name"],
                                                   middle_name=form.cleaned_data["middle_name"],
                                                   last_name=form.cleaned_data["last_name"],
                                                   mobile=form.cleaned_data["mobile"],
                                                   password=form.cleaned_data["password"]
                                                   )
        user_details.save()
        millis = time.mktime(datetime.now().timetuple())
        payload = {'user': {"email": form.cleaned_data["email"],
                            "password": form.cleaned_data["password"],
                            "mobile": form.cleaned_data["mobile"],
                            "first_name": form.cleaned_data["first_name"]},
                   'iat': millis, 'exp': millis + 43200}
        try:
            user = authenticate(email=request.POST.get("email", ""), password=request.POST.get("password", ""))
            login(request, user)
        except Exception, e:
            print e
        return Response({'token': AuthUtil.encrypt(jwt_encode_handler(payload)),
                         'user': form.cleaned_data["first_name"]},
                        status=status.HTTP_200_OK)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    user = authenticate(email=request.POST.get("email", ""), password=request.POST.get("password", ""))
    print user
    if user is not None:
        if user.is_active:
            try:
                user_data = AppUser.objects.get(email=request.POST.get("email"))
                millis = time.mktime(datetime.now().timetuple())
                payload = {'user': {"email": request.POST.get("email", ""),
                                    "password": request.POST.get("password", ""),
                                    "mobile": user_data.mobile,
                                    "first_name": user_data.first_name},
                           'iat': millis, 'exp': millis + 43200}
                # print payload
                # login(request, user)

            except Exception, e:
                return Response({"message": "Error in the login process"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'token': AuthUtil.encrypt(jwt_encode_handler(payload)),
                             'user': user_data.first_name},
                            status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def request_otp(request):
    params = request.POST.get("params")
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if len(params) == 10 and params.isdigit():
        try:
            user_details = AppUser.objects.get(mobile=int(params))
        except Exception, e:
            user_details = None
        if user_details:
            # send_otp(user_details)
            return Response({"message": "OTP sent to mobile", "user_id": user_details.id}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not registered"}, status=status.HTTP_400_BAD_REQUEST)

    elif email_regex.match(str(params)):
        try:
            user_details = AppUser.objects.get(email=params)
        except Exception, e:
            user_details = None

        if user_details:
            OTP = randint(1000, 9999)
            user_details.otp = 5555
            user_details.save()
            return Response({"message": "OTP sent to email", "user_id": user_details.id}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not registered"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "User Details invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def forget_password(request):
    otp = request.POST.get("otp")
    password = request.POST.get("password")
    try:
        detail = AppUser.objects.get(id=request.POST.get("id"))
    except Exception:
        detail = None
    if detail:
        if int(detail.otp) == int(otp):
            update_password = make_password(password)
            detail.password = update_password
            detail.save()

            user = authenticate(email=detail.email, password=request.POST.get("password", ""))
            if user is not None:
                if user.is_active:
                    try:
                        user_data = AppUser.objects.get(email=detail.email)
                        # print user_data.email, user_data.mobile, user_data.full_name
                        millis = time.mktime(datetime.now().timetuple())
                        payload = {'user': {"email": user_data.email,
                                            "password": request.POST.get("password", ""),
                                            "mobile": user_data.mobile,
                                            "first_name": user_data.first_name},
                                   'iat': millis, 'exp': millis + 43200}
                        # print payload
                        login(request, user)
                    except Exception, e:
                        return Response({"message": "Error in the login process"}, status=status.HTTP_400_BAD_REQUEST)

                    return Response({'token': AuthUtil.encrypt(jwt_encode_handler(payload)),
                                     'user': user_data.first_name,
                                     'message': "Password Updated"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Wrong OTP"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@jwt_decorator
def logout_user(request, *args, **kwargs):
    try:
        logout(request)
        return Response({"message": "User logged out."}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

