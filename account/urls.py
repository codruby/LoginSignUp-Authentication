from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from .views import signup_user, logout_user, login_user, request_otp, \
    forget_password #resend_otp
from rest_framework.authtoken import views as rest_framework_views
# from .views import CustomObtainAuthToken
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^signup/$', signup_user, name='test_signUp'),
    # url(r'^resend_otp/', resend_otp, name="resend_otp"),
    url(r'^signin/$', login_user, name='signIn'),
    url(r'^logout/$', logout_user, name='logOut'),
    # url(r'^authenticate/', authenticate_user, name="authenticate"),
    url(r'^request_otp/', request_otp, name="request_otp"),
    url(r'^forget_password/', forget_password, name="forget_password"),

]