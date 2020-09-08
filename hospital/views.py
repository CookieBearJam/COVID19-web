import csv
import os

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from hospital.models import Hospital

# LOCATION = {'吉林省': {'长春市': ['南关区', '朝阳区', '二道区', '绿园区']}}
STRING_LOCATION = {}  # 解析得到xml文件中的名字（key为单个字符串）
CODED_LOCATION = {}  # 用于记录确切的地理编码（key为元组）


# 使用相应的url来调用相应的函数
def index(request):
    # 初始化数据，这个要放到其他的地方执行
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
    # 判断上传的数据是否有误，存储实例模型


def choose_province(request):
    province = list(STRING_LOCATION.keys())
    return JsonResponse(province, safe=False)


def choose_city(request):
    province = request.GET.get('p')
    cities = list(STRING_LOCATION[province].keys())
    return JsonResponse(cities, safe=False)


def choose_district(request):
    province = request.GET.get('p')
    city = request.GET.get('c')
    districts = STRING_LOCATION[province][city]
    return JsonResponse(districts, safe=False)


# 测试通过省市区查找当前的编码，打印函数
def print_specified_dict(coded_location):
    if isinstance(coded_location, dict):
        for p, c_dict in coded_location.items():
            print("(", p[0], ",", p[1], ")\n")
            if isinstance(c_dict, dict):
                for c, d_dict in c_dict.items():
                    print("\t(", c[0], ",", c[1], ")\n")
                    if isinstance(d_dict, dict):
                        for d, code in d_dict.items():
                            print("\t\t", d, ":", code, "\n")  # 打印key和value


def search_code_by_name(coded_location, province, city, district):
    code_list = []  # 用一个list把编码传回去
    for p, c_dict in coded_location.items():
        if province == p[0]:
            code_list.append(p[1])
            for c, d_dict in c_dict.items():
                if city == c[0]:
                    code_list.append(c[1])
                    for d, code in d_dict.items():
                        if district == d:
                            code_list.append(code)
    return code_list


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

    # 带有地理位置编码的部分临时变量
    temp_province_dict_specified = {}
    temp_city_dict_specified = {}
    temp_district_dict = {}

    for province in root.iter("p"):
        for city in province.iter("c"):
            for district in city.iter("d"):
                if district.text == city.find("cn").text and (len(city.findall("d")) != 1):
                    continue  # 不添加名字与区相同的市
                temp_district_list.append(district.text)
                temp_district_dict.update({district.text: district.get("d_id")})
            # print("没有编码", temp_district_list)
            # print("添加编码", temp_district_dict)
            temp_city_dict.update({city.find("cn").text: temp_district_list})
            temp_city_dict_specified.update({(city.find("cn").text, city.get("c_id")): temp_district_dict})
            temp_district_list = []
            temp_district_dict = {}
        # print("没有编码", temp_city_dict)
        # print("添加编码", temp_city_dict_specified)
        temp_province_dict.update({province.find("pn").text: temp_city_dict})
        temp_province_dict_specified.update(
            {(province.find("pn").text, province.get("p_id")): temp_city_dict_specified})
        temp_city_dict = {}
        temp_city_dict_specified = {}
    # print("没有编码", temp_province_dict)
    # print("添加编码", temp_province_dict_specified)
    STRING_LOCATION.update(temp_province_dict)
    CODED_LOCATION.update(temp_province_dict_specified)

    # print_specified_dict(CODED_LOCATION)
