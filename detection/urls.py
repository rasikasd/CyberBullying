from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='detection-home'),
    path('about/', views.about, name='detection-about'),
    path('dashboard/', views.dashboard, name='detection-dashboard'),
    path('moderate/', views.moderate, name='detection-moderate'),
]