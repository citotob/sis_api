from django.urls import path
from . import views
#from sites import views as sites_views
#from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('respon/', views.respon),
    path('penawaran/', views.penawaran),
    path('getbatch/', views.getbatch),
    #path('getsite/', sites_views.getsite),
    path('getvendorapp/', views.getVendorApp),
    path('getallvendor/', views.getallvendor),
]
