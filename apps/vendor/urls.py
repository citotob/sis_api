from django.urls import path
from vendor import views
from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('respon/', views.respon),
    path('penawaran/', views.penawaran),
    path('getbatch/', views.getbatch),
    path('getsite/', views.getsite),
]
