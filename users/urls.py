from django.urls import path, include
from .views import login_view, otp_view, logout_view, main_view, LoginApi, add_ref, OTPApi, ProfileApi

urlpatterns = [
    path('', login_view, name='login'),
    # path('<str:ref_code>/', main_view, name='main'),
    path('profile/', main_view, name='main'),
    path('otp/', otp_view, name='otp'),
    path('logout/', logout_view, name='logout'),

    path('add/', add_ref, name='add_ref'),

    path('login', LoginApi.as_view()),
    path('login/otp', OTPApi.as_view()),
    path('login/profile', ProfileApi),

]
