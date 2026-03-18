from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/avatar/', views.avatar_upload_view, name='avatar_upload'),
    path('profile/cover/', views.cover_upload_view, name='cover_upload'),
    path('settings/privacy/', views.privacy_settings_view, name='privacy_settings'),
]
