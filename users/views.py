from django.contrib import auth
from users.utils.jwt import encode_jwt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
# from django.contrib.auth import login as auth_login
from django.contrib.auth.models import AnonymousUser

import datetime
from users.utils.jwt import encode_jwt
from json import loads

from .models import *
from .forms import *
import json, datetime
from orders.models import *
import pdb

# 프로필 페이지
def main(request, id):
    user_profile = get_object_or_404(User, pk=id)

    if request.user == user_profile:
        return render(request, 'users/main.html', {'user_profile': user_profile})
    return redirect('main')

# 캘린더 페이지
def schedule(request, id):
    current_user = request.user
    user = get_object_or_404(User, pk=id)
    
    if user == request.user:
        all_orders = Order.objects.filter(user=user).filter(isValid=True)
        orders_list = []

        for order in all_orders:
            parsed_date = order.created_at.strftime(f'%Y-%m-%d')
            orders_list.append({
              "title": order.collection_name,
              "start": parsed_date,
              "period":order.period,
            },)

        jsonString = json.dumps(orders_list) # json 변환

        return render(request, 'users/schedule.html', {'all_orders':jsonString})
    return redirect('users:schedule', current_user.id)

# 프로필 수정 페이지
@login_required
def edit(request, id):
    current_user = request.user
    user = get_object_or_404(User, pk=id)

    if user == current_user:
        if user.username == 'testuser':
            return redirect('users:main', current_user.id)
        else:
            return render(request, 'users/edit.html', {'user': user})
    else:
        return redirect('users:main', current_user.id)


# 프로필 수정
@login_required
def update(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=id)
        nickname = request.POST.get('nickname')
        phone = request.POST.get('phone')
        profile_address = request.POST.get('profile_address')
        
        if request.FILES.get('profile_image'):
            user.profile.profile_image = request.FILES.get('profile_image')
            
        if request.POST.get('checkbox'):
            user.profile.profile_image = 'images/default_profile.jpg'


        user.profile.nickname = nickname
        user.profile.phone = phone
        user.profile.profile_address = profile_address

        user.profile.address1 = request.POST.get('b')
        user.profile.address2 = request.POST.get('d')
        user.profile.detail_address = request.POST.get('c')
        user.profile.zipcode = request.POST.get('a')

        user.profile.save()
        return redirect('users:main', id)

# 프로필 삭제 
@require_POST
@login_required
def delete(request):

    user = request.user
    user.is_active = False
    user.save()

    response = redirect('main')
    response.delete_cookie('jwt')

    return response

# JWT 토큰 발행
def generate_access_token(username):
    # 토큰 발행일
    iat = datetime.datetime.now()
    # 토큰 만료일
    exp = iat + datetime.timedelta(days=7)

    data = {
        "iat" : iat.timestamp(),
        "exp" : exp.timestamp(),
        "aud" : username,
        "iss" : "LOHBS_PICK Web Backend"
    }
    
    return encode_jwt(data)

def login_page(request):
    form = AuthenticationForm
    return render(request, 'account/login.html', {'form':form})

# login기능
def login(request):
    data ={}
    form = AuthenticationForm

    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        
        if user:
            token = generate_access_token(username)

            if user.is_active:
                # auth_login(request, user)
                # user.is_active = True

                response = redirect('main')
                response.set_cookie(key="jwt", value=token, httponly=True)

                # pdb.set_trace()
                return response
        else:
            p = "아이디 혹은 비밀번호가 틀렸습니다."    
            return render(request, 'account/login.html', {'form':form, 'p' : p})

    return redirect(login_page)

# logout 기능
def logout(request):
    
    if request.method == "POST":

        response = redirect('main')
        response.delete_cookie('jwt')

        return response 

    else:
        return render(request, 'account/logout.html')
