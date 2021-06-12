from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index),
    path('recommend/', views.recommend),
    path('<int:user_id>/recommend/',views.user_recommend),
    path('<int:movie_id>/',views.movie_detail),
    path('naver/<int:movie_id>/',views.naver_movie_detail),
    path('boxoffice/<int:movie_id>/',views.boxoffice_movie_detail),
    path('<int:movie_id>/like/',views.like),
    path('<int:movie_id>/comments/', views.comment_create),
    path('comments/', views.comment_list),
    path('comments/<int:comment_id>/', views.comment_detail), 
]