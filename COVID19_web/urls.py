"""COVID19_web URL Configuration

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
from django.urls import path

from hospital import views

# from hospital.views import choose_province, choose_city, choose_district
from hospital.views import choose_province, choose_city, choose_district

urlpatterns = [
    path('province/', choose_province),
    path('city/', choose_city),
    path('district/', choose_district),

    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('upload/', views.upload, name='upload'),  # name用于匹配html中的直接跳转
    path('hospital_login/', views.hospital_login, name='hospital_login'),
    path('hospital_login/confirmed', views.hospital_confirmed, name='hospital_confirmed'),
]
