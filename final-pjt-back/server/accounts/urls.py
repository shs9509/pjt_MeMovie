from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', obtain_jwt_token),
    path('profile/<int:user_pk>/', views.profile, name='profile'),
    path('follow/<int:user_pk>/', views.follow, name='follow'),
]
