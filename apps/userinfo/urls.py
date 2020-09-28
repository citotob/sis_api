from django.urls import path
from userinfo import views
from rest_framework.authtoken import views as tokenview

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('login/', views.login),
    path('get/', views.getUser),
    path('getbyrole/', views.getUserByRole),
    path('verify/', views.verifyUser),
    path('decline/', views.declineUser),
    path('removeuser/', views.removeuser),
    path('regist/', views.register),  # register
    # path('register/', views.register),  # register
    path('addrole/', views.createRole),
    path('getrole/', views.getRole),
    path('getstaffsurvey/', views.getStaffSurvey),
    path('changepassword/', views.changepassword),

    path('sendmail/', views.sendmail),
    path('test/', views.test),

    path('getnotif/', views.getnotif),
    path('sendnotif/', views.sendnotif),

    path('updatesurveyor/', views.updatesurveyor),

]
