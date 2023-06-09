"""lohbs_pick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
import users.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('accounts/login/', users.views.login, name="login"),
    path('accounts/logout/', users.views.logout, name="logout"),
    path('login_page/', users.views.login_page, name="login_page"),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('picks/', include('picks.urls')),
    path('orders/', include('orders.urls')),
    path('personal_data/', views.personal_data, name="personal_data"),
    path('service_terms/', views.service_terms, name="service_terms"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
