from django.urls import path
from sites import views
from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('addbatch/', views.addbatch),
    path('addsite/', views.addsite),
    path('editbatch/', views.editbatch),
    path('uploadsite/', views.uploadsite),
]
