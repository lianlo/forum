from django.urls import path
from .views import *


urlpatterns = [
    path('', QuestionsList.as_view(), name='questions_list_url'),
    path('question/create/', QuestionCreate.as_view(), name='question_create_url'),
    path('question/<str:slug>/', QuestionDetail.as_view(), name='question_detail_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name='tag_detail_url'),
]