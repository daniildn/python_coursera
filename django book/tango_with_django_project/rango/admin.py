# Register your models here.
from django.contrib import admin
from rango.models import Category, Page
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name', 'likes', "views", "slug")
admin.site.register(Category, CategoryAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'category')


admin.site.register(Page, PageAdmin)
