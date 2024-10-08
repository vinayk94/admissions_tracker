from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('api/like/<int:post_id>/', views.like_post, name='like_post'),
    path('api/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('api/reply/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('api/comments/<int:post_id>/', views.get_comments, name='get_comments'),
    path('api/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('', views.admission_dashboard, name='admission_timeline'),
    path('stats/', views.AdmissionStatsView.as_view(), name='admission_stats'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]