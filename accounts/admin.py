from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("name",)}


class InterestsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':("title",)}


admin.site.register(Reader)
admin.site.register(Bloger)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Interests,InterestsAdmin)
