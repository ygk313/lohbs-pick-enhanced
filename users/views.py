from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

from .models import *
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
    # request.user.delete()
    user = request.user
    user.is_active = False
    user.save()

    logout(request)
    return redirect('main')

# login기능
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
    
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('main')
        else:
            p = "아이디 혹은 비밀번호가 틀렸습니다."    
            form = AuthenticationForm
            return render(request, 'account/login.html', {'form':form, 'p' : p})
    else:
        form = AuthenticationForm
    return render(request, 'account/login.html', {'form':form})