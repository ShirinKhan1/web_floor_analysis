from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_page, name='home'),
    path('monitoring/', views.monitoring_page, name='monitoring_page'),
    path('parsing/', views.parsing_page, name='parsing_page'),
    path('calcai/', views.calculator_page, name='calculator_page'),
    path('analysis/', views.analysis_district, name='analysis_district'),
    path('checking/', views.check_district, name='check_district')
]
