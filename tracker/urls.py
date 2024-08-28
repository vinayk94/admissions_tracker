from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.admission_dashboard, name='admission_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('api/like/<int:post_id>/', views.like_post, name='like_post'),
    path('api/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('logout/', LogoutView.as_view(), name='logout'),
]