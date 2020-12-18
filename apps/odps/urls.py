from django.urls import path
from . import views
#from rest_framework.authtoken import views as tokenview


urlpatterns = [
    path('uploadodp/', views.uploadodp),
    path('uploadodpbackup/', views.uploadodp1),
    path('getodp/', views.getRecommendTech),
    path('addodp/', views.addodp),
    path('get/', views.getodp),

    path('uploadbts/', views.uploadbts),
    
]
