from django.contrib import admin
import xadmin

from .models import  CityDict,CourseOrg,Teacher
# Register your models here.

class CityDictAdmin():
    list_display = ["name","desc","add_time"]
    search_fields = ["name","desc"]
    list_filter = ["name","desc","add_time"]



xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg)
xadmin.site.register(Teacher)
