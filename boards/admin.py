from django.contrib import admin
from .models import *


class BoardAdmin(admin.ModelAdmin):
    list_display = ["id","name","description"]
    list_display_links= ["id","name"]


# class TopicAdmin(admin.ModelAdmin):
#     list_display = ["id","subject"]
#     list_display_links= ["id","subject"]
    

admin.site.register(Board,BoardAdmin)
admin.site.register(Topic)
admin.site.register(Post)

