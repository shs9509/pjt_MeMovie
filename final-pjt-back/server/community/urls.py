from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.review_list),
    path('reviews/', views.review_create),
    path('reviews/<int:review_id>/', views.review_detail),
    path('reviews/<int:review_id>/change/', views.review_change),
    path('reviews/<int:review_id>/comments/', views.comment_create),
    path('comments/<int:comment_id>/', views.comment_detail),
]