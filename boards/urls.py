from django.urls import path
from .views import *


urlpatterns = [
        path('',BoardListView.as_view(), name='home'),
        path('topics/<int:pk>/', TopicListView.as_view(), name='board_topics'),
        path('boards/<int:pk>/new/', New_topicView.as_view(), name='new_topic'),
        path('boards/<int:pk>/topics/<int:topic_pk>/', PostListView.as_view(), name='topic_posts'),
        path('boards/<int:pk>/topics/<int:topic_pk>/reply/',reply_topic, name='reply_topic'),
######################################################################################################################
        path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/', PostUpdateView.as_view(), name='edit_post'),
        path('new_articles/',new_articles,name='new_articles'),
        path('boards/fake/', generate_fake_data, name='generate_fake_data'),
                path('boards/create/',board_create, name='boards_create'),
                path('boards/<int:pk>/update/', board_update, name='boards_update'),
                path('boards/<int:pk>/delete/', board_delete, name='boards_delete'),
        path('boards/<int:pk>/to-xls/',export_boards_xls,name='to-xls'),
        path('boards/<int:pk>/to-pdf/',export_boards_pdf,name='to-pdf')
]