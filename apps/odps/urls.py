from django.urls import path
from . import views
#from rest_framework.authtoken import views as tokenview


urlpatterns = [
    path('uploadodp/', views.uploadodp),
    
]
