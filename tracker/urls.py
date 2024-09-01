from django.urls import path
from . import views

urlpatterns = [
    path('', views.admission_dashboard, name='admission_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/like/<int:post_id>/', views.like_post, name='like_post'),
    path('api/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('api/reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('api/comments/<int:post_id>/', views.get_comments, name='get_comments'),
]