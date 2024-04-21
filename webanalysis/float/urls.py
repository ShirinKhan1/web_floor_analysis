from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_page),
    path('monitoring/', views.monitoring_page, name='monitoring_page'),
    path('parsing/', views.parsing_page, name='parsing_page'),
    path('profile/', views.profile_page),
    path('register/', views.register_page),
    path('login/', views.login_page),
    path('calcai/', views.calculator_page)
]
