from django.urls import path
from . import views
#from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('addbatch/', views.addbatch),
    path('addsite/', views.addsite),
    path('editbatch/', views.editbatch),
    path('uploadsite/', views.uploadsite),
    path('getbatch/', views.getbatch),
    path('getallbatch/', views.getallbatch),

    path('sendinvitation/', views.sendinvitation),
    
    path('dashboard/', views.getDashboard),

    path('uploadsiteoffair/', views.uploadsiteoffair),
    path('getoffair/', views.getsiteoffair),
    path('checknearoffair/', views.checknearsiteoffair),
    path('getlistoffair/', views.getoffairid),
    path('getoffairbyid/', views.getoffairbyid),
    path('getoffairprovinsi/', views.getoffairprovinsi),
    path('getoffaircluster/', views.getoffaircluster),
    path('validatebatchsites/', views.validatebatchsites),

    path('calculatevendorscore/', views.calculatevendorscore),

    path('cloneoffair/', views.clonesiteoffair),
    path('getrecommendvendor/', views.getvendorcluster),
    path('syncsiteoffair/', views.syncsiteoffair),


]
