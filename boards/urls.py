from django.urls import path
from .views import *


urlpatterns = [
        path('',BoardListView.as_view(), name='home'),
        path('boards/<int:pk>/', TopicListView.as_view(), name='board_topics'),
        path('boards/<int:pk>/new/', new_topic, name='new_topic'),
        path('boards/<int:pk>/topics/<int:topic_pk>/', PostListView.as_view(), name='topic_posts'),
        path('boards/<int:pk>/topics/<int:topic_pk>/reply/',reply_topic, name='reply_topic'),
######################################################################################################################
        path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/', PostUpdateView.as_view(), name='edit_post'),
        path('new_articles/',new_articles,name='new_articles')
]