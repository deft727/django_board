from django.contrib import admin
from .models import *


class RaderAdmin(admin.ModelAdmin):
    list_display= ( 'id','username','user')
    list_display_links=('id','username','user')


class BlogerAdmin(admin.ModelAdmin):
    list_display= ( 'id','username','user')
    list_display_links=('id','username','user')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}


class InterestsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}


admin.site.register(Reader,RaderAdmin)
admin.site.register(Bloger,BlogerAdmin)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Interests,InterestsAdmin)
