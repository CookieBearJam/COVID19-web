from xml.etree import ElementTree

# 最终需要解析成的数据形式
# 最后在save_model的时候需要反向查找编码，所以需要同时创建一个带有编码的列表
LOCATION = {
    '吉林省': {'长春市': ['南关区', '朝阳区', '二道区', '绿园区'], '吉林市': ['中心区']},  # 省，dict，一个省有许多个市# 市，dict # 区，列表，
    '湖南省': {'长沙市': ['长沙县', '雨花区']}
}

CODED_LOCATION = {}  # 用于记录确切的地理编码

location_list = {}  # 以元组作为key的字典，三层嵌套


# 测试通过省市区查找当前的编码
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


if __name__ == "__main__":
    filename = "citylist_2.xml"
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
    location_list.update(temp_province_dict)
    CODED_LOCATION.update(temp_province_dict_specified)

    print_specified_dict(CODED_LOCATION)

    print(search_code_by_name(CODED_LOCATION, "海南", "海口", "海口"))
    print(search_code_by_name(CODED_LOCATION, "香港", "香港", "九龙"))
    print(search_code_by_name(CODED_LOCATION, "黑龙江", "牡丹江", ""))
    print(len(search_code_by_name(CODED_LOCATION, "黑龙", " ", "")))
