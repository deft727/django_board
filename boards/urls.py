from django.urls import path
from .views import *


urlpatterns = [
        path('',home,name='home'),
        path('boards/<int:pk>/', board_topics, name='board_topics'),
        path('boards/<int:pk>/new/', new_topic, name='new_topic'),


]