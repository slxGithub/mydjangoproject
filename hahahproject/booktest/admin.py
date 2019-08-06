from django.contrib import admin

from .models import BookInfo, HeroInfo

# Register your models here.


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','btitle','bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'hname','hgender','hcomment']

# 注册模型类,
admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(HeroInfo,HeroInfoAdmin)
