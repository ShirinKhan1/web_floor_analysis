from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUSer.as_view(), name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('method/<int:method_id>/', views.method, name='method'),
    path('register/', views.RegisterUSer.as_view(), name='register'),
    path('not_authenticated/', views.not_authenticated, name='not_auth')
]
