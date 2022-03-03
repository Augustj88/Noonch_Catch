from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:room_name>/', views.room, name='room'),
    path('ending/', views.ending, name='ending'),
    path('user/', views.get_user, name='user'),
    path('test1/', views.post_pic),
]

