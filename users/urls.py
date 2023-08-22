from django.urls import path
from .views import login_view, otp_view, logout_view, main_view, LoginApi, OTPApi, ProfileApi,add_ref

urlpatterns = [
    path('', login_view, name='login'),
    path('profile/', main_view, name='main'),
    path('otp/', otp_view, name='otp'),
    path('logout/', logout_view, name='logout'),
    path('add/', add_ref, name='add_ref'),
    # API
    path('login', LoginApi.as_view()),
    path('login/otp', OTPApi.as_view()),
    path('login/profile', ProfileApi),
]
