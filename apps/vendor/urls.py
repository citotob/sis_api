from django.urls import path
from . import views
#from sites import views as sites_views
#from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('respon/', views.respon),
    path('penawaran/', views.penawaran),
    path('rfi/', views.penawaran_),
    path('checkrfibatch/', views.checkRfiBatch),
    path('checkrfivendor/', views.checkRfiVendor),
    path('checkjudul/', views.checkJudul),
    path('getbatch/', views.getbatch),
    #path('getsite/', sites_views.getsite),
    path('getvendorapp/', views.getVendorApp),
    path('getallvendor/', views.getallvendor),
    path('dashboard/', views.getDashboardData),
]
