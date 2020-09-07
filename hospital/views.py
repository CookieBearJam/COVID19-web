import csv
import os

import pymysql
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from hospital.models import Hospital

# LOCATION = {'吉林省': {'长春市': ['南关区', '朝阳区', '二道区', '绿园区']}}
LOCATION = {}


# 使用相应的url来调用相应的函数
def index(request):
    # 初始化数据
    filename = "static/city.xml"
    get_data(filename)
    return render(request, 'index.html')


def hospital_login(request):
    return render(request, 'hospital_login.html')


# 医院用户身份认证入口
def hospital_confirmed(request):
    a = request.GET
    username = a.get('username')
    password = a.get('password')
    # print(username)
    # print(password)
    identified = hospital_identify(username, password)
    if identified == 1:  # 验证成功则渲染upload页面
        render(request, 'upload.html')
        return HttpResponseRedirect('/upload')
    elif identified == 0:
        render(request, 'hospital_login.html')
        return HttpResponseRedirect('/hospital_login')  # 登录信息验证失败，重定向回到login页面，不发生改变
    else:
        return render(request, 'fail.html')  # 验证失败就渲染失败页面


# 医院用户身份认证DAO
def hospital_identify(username, password_):
    result = Hospital.objects.filter(username=username)  # 找出该用户的记录
    if result.exists():  # 有这个用户
        hospital = result.first()
        password = hospital.passwd
        if password == password_:
            print("验证成功，用户已授权")
            return 1
        else:
            print("密码错误")
            return 0
    else:
        print("医院用户名错误")
        return -1


# 疫情上报界面的处理逻辑
def upload(request):
    if request.method == "POST":  # 请求方法为POST时，进行处理
        files = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not files:
            return HttpResponse("no files for upload!")
        # 上传到static中的upload文件夹
        destination = open(os.path.join("./static/upload", files.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        # 如果文件大于2.5MB使用chunks分块
        for chunk in files.chunks():
            destination.write(chunk)
        destination.close()

        filename = files.name
        parse_csv(os.path.join("./static/upload", filename))
        render(request, 'upload.html')
        return HttpResponseRedirect('/upload')
    else:
        return render(request, 'upload.html')


def parse_csv(filepath):
    with open(filepath, 'r') as f:
        csv_reader = csv.reader(f)
        rows = [row for row in csv_reader]
        print(rows)
    # 判断上传的数据是否有误


def choose_province(request):
    province = list(LOCATION.keys())
    return JsonResponse(province, safe=False)


def choose_city(request):
    province = request.GET.get('p')
    cities = list(LOCATION[province].keys())
    return JsonResponse(cities, safe=False)


def choose_district(request):
    province = request.GET.get('p')
    city = request.GET.get('c')
    districts = LOCATION[province][city]
    return JsonResponse(districts, safe=False)


# 从xml文件读取数据存储到字典中
def get_data(filename):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET

    tree = ET.parse(filename)
    root = tree.getroot()

    temp_province_dict = {}
    temp_city_dict = {}
    temp_district_list = []
    for province in root.iter("p"):
        for city in province.iter("c"):
            for district in city.iter("d"):
                temp_district_list.append(district.text)
            print(temp_district_list)
            temp_city_dict.update({city.find("cn").text: temp_district_list})
            temp_district_list = []
        print(temp_city_dict)
        temp_province_dict.update({province.find("pn").text: temp_city_dict})
        temp_city_dict = {}
    print(temp_province_dict)
    LOCATION.update(temp_province_dict)
