from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login

from django.contrib.auth.decorators import login_required
from rest_framework.decorators import permission_classes, api_view

from .utils import send_opt
from datetime import datetime
import pyotp

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework.permissions import IsAuthenticated


def login_view(request):
    if request.method == 'POST':
        username = request.POST['phone']
        user = CustomUser.objects.filter(phone=username).first()
        if user is not None:
            send_opt(request)
            request.session['phone'] = username
            return redirect('otp')
        else:
            user = CustomUser.objects.create(phone=username)

            profile = Profile.objects.create(user=user)
            print(user, profile)
            send_opt(request)
            request.session['phone'] = username
            return redirect('otp')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required()
def main_view(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommended_profiles()
    rec_by = profile.recommended_by
    code = profile.code
    error = None
    try:
        if request.session['error']:
            error = request.session['error']
    except:
        pass
    context = {'my_recs': my_recs, 'rec_by': rec_by, 'code': code, 'error_message': error}

    return render(request, 'main.html', context)


@login_required()
def add_ref(request):
    code = request.POST['code_sent']
    invited_by = Profile.objects.filter(code=code)
    if not invited_by:
        request.session['error'] = 'Пользователь с таким кодом не найден. Повторите.'
        return redirect('main')
    else:
        invited_by = Profile.objects.get(code=code)
    username = request.user
    user = CustomUser.objects.get(phone=username)
    if code == user.profile.code:
        request.session['error'] = 'Нельзя вводить свой код. Повторите'
        return redirect('main')
    user.profile.recommended_by = invited_by.user
    user.profile.save(update_fields=["recommended_by"])
    return redirect('main')


def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['phone']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(CustomUser, phone=username)
                    login(request, user)
                    try:
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                    except:
                        pass
                    return redirect('main')
                else:
                    error_message = 'invalid OTP'
            else:
                error_message = 'OTP has expired'
        else:
            error_message = 'error'
    return render(request, 'otp.html', {'error_message': error_message})


class LoginApi(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            phone = request.data.get('phone')
            user = CustomUser.objects.get(phone=phone)
            profile = Profile.objects.create(user=user)
            otp = send_opt(request)
            request.session['phone'] = phone
            return Response({
                'message': 'User created. Sending OTP.',
                'otp': otp,
            }, status=status.HTTP_200_OK)
        else:
            phone = serializer.data['phone']
            request.session['phone'] = phone
            user = CustomUser.objects.filter(phone=phone)
            if user.exists():
                otp = send_opt(request)
                return Response({
                    'message': 'Sending OTP',
                    'otp': otp,
                }, status=status.HTTP_200_OK)


class OTPApi(APIView):
    def post(self, request):
        error = None
        phone = request.data['phone']
        user = get_object_or_404(CustomUser, phone=phone)
        if not user:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        otp = request.data['otp']
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
            error = 'OTP is expired'
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(CustomUser, phone=phone)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    return Response({
                        'message': 'успешно',
                    }, status=status.HTTP_200_OK)
                error = 'OTP is not correct'
        return Response({
            'message': error,
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def ProfileApi(request):
    phone = request.session['phone']
    user = CustomUser.objects.get(phone=phone)
    profiles = Profile.objects.get(user=user)
    my_recs = profiles.get_recommended_profiles()
    data = []
    for p in my_recs:
        data.append(p.user)
    serializer = UserSerializer(data, many=True)
    return JsonResponse({'Вы пригласили': serializer.data}, status=status.HTTP_200_OK)
