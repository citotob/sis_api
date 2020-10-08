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

    path('addodp/', views.addodp),
    path('getodp/', views.getRecommendTech),
]
