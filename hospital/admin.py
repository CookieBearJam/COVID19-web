from django.contrib import admin
from django import forms
from hospital.views import search_code_by_name, CODED_LOCATION

from hospital.models import Hospital, Patient, Pstatus, Supplies, Track

# Register your models here.

admin.site.site_header = '疫情防控管理平台'
object_per_page = 8  # 规定每个页面展示的对象数量


# 新建医院的时候需要同时新建一条除了关联医院id之外，全都为0的supplies记录,这是医院管理类
class PstatusAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'status', 'day']
    # search_fields = ['p_id', 'status', 'day']
    list_per_page = object_per_page


class PstatusInline(admin.StackedInline):
    model = Pstatus


class PatientAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'h_id', 'no', 'tel', 'username', 'status']
    # search_fields = ['no']
    inlines = [PstatusInline, ]
    list_per_page = object_per_page


# 这是物资编辑的管理类
class TrackAdmin(admin.ModelAdmin):
    list_display = ['p_id', 'date_time', 'longitude', 'latitude', 'description', 'location', 'district']
    # search_fields = ['district']
    list_per_page = object_per_page


# 需要同时创建一个物资记录于是添加一个内联类
class SuppliesInline(admin.StackedInline):
    model = Supplies


class SuppliesAdmin(admin.ModelAdmin):
    list_display = ['h_id', 'n95', 'surgeon', 'ventilator', 'clothe', 'glasses', 'alcohol', 'pants']
    list_per_page = object_per_page


class HospitalForm(forms.ModelForm):
    class Meta:
        widgets = {
            'province': forms.Select(),
            'city': forms.Select(),
            'district': forms.Select()
        }


class HospitalAdmin(admin.ModelAdmin):
    form = HospitalForm
    inlines = [SuppliesInline, ]
    list_per_page = object_per_page
    fieldsets = [
        (None, {'fields': ['name', 'address', 'tel', 'contact', 'username', 'passwd', 'mild_left', 'severe_left']}),
        (None, {'fields': ['province', 'city', 'district']})
    ]
    list_display = ['h_id', 'name', 'address', 'tel', 'contact', 'username', 'passwd', 'mild_left', 'severe_left',
                    'province', 'city', 'district']

    change_form_template = 'area.html'  # 为了使用模板

    # 重写保存model的函数以实现创建触发器
    def save_model(self, request, obj, form, change):
        if form.is_valid():
            code_list = search_code_by_name(CODED_LOCATION, obj.province, obj.city, obj.district)
            if len(code_list) == 3:
                obj.province = code_list[0]
                obj.city = code_list[1]
                obj.district = code_list[2]

            # 在创建医院的时候同时创建一个supply
            hospital = form.save()
            supplies = Supplies()
            supplies.h = hospital
            supplies.save()

        super().save_model(request, obj, form, change)


# 注册模型到管理类
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Pstatus, PstatusAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Supplies, SuppliesAdmin)
