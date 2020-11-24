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
    
    path('dashboard/', views.getDashboard),

    path('uploadsiteoffair/', views.uploadsiteoffair),
    path('getoffair/', views.getsiteoffair),
    path('getlisoffair/', views.getsiteoffairid),
    path('getoffairbyid/', views.getoffairbyid),
    path('getoffairprovinsi/', views.getoffairprovinsi),

    path('calculatevendorscore/', views.calculatevendorscore),


]
