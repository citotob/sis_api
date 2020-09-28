from Location import views
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('provinsi/', views.getAllProvinsi),
    path('kabupatenkota/', views.getKabupaten),
    path('kecamatan/', views.getKecamatan),
    path('desa/', views.getDesa),
]
