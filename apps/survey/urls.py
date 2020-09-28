from django.urls import path
from survey import views
from rest_framework.authtoken import views as tokenview


urlpatterns = [
    # path('login/', tokenview.obtain_auth_token),
    path('addjenissurvey/', views.addjenissurvey),
    path('getjenissurvey/', views.getjenissurvey),

    path('addsurveyor/', views.addsurveyor),
    path('getsurveyor/', views.getsurveyor),

    path('addlokasisurvey/', views.addlokasisurvey),
    path('getlokasisurvey/', views.getlokasisurvey),
    path('uploadlokasi/', views.uploadlokasi),
    path('uploadlokasikodesurvey/', views.uploadlokasikodesurvey),

    path('addpenugasan/', views.addpenugasan),
    path('editpenugasan/', views.editpenugasan),
    path('getpenugasan/', views.getpenugasan),
    path('getpenugasan/count/', views.countPenugasan),
    path('getpenugasan/count/daily', views.countPenugasanDaily),
    path('getpenugasan/count/provinsi', views.countPenugasanProvinsi),
    path('assignpenugasan/', views.assignpenugasan),
    path('changestatuspenugasan/', views.changestatuspenugasan),
    path('uploadspk/', views.uploadspk),
    path('getpenugasansurveyor/', views.getpenugasansurveyor),

    path('addHasilSurvey/', views.PosthasilSurvey),
    path('getsurvey/', views.getAllHasilSurveyByKode),
    # path('getsurveybyuser/ai/', views.getHasilSurveyByUserIdAI),
    path('getsurveybyuser/ai/', views.getHasilSurveyByUserAI),
    path('getsurveybyuser/ai/detail/', views.getHasilSurveyByUserIdAIdetail),
    # path('getsurveybyuser/bts/', views.getHasilSurveyByUserIdBTS),
    path('getsurveybyuser/bts/', views.getHasilSurveyByUserBTS),
    path('getsurveybyuser/bts/detail/', views.getHasilSurveyByUserIdBtsdetail),
    path('getsurveybts/', views.getsurveystatusai),
    path('changestatusai/', views.changeStatusAI),
    path('changestatusbts/', views.changeStatusBTS),
    path('addhasilsurveybts/', views.postBTS),
    path('getsurveystatusai/', views.getsurveystatusai),
    path('getsurveystatusbts/', views.getsurveystatusbts),
    path('getsurveybydateai/', views.getsurveybydateai),
    path('getsurveybydatebts/', views.getsurveybydatebts),
    path('getsurveyaibyid/', views.getHasilSurveyAiById),
    path('getsurveybtsbyid/', views.getHasilSurveyBtsById),
    path('declinesurvey/', views.declinesurvey),
    path('approvesurvey/', views.approvesurvey),
    path('setujuisurvey/', views.setujuisurvey),
    path('tandaisurvey/', views.tandaisurvey),
    path('getsurveyissue/', views.getsurveyissue),
    path('getissuebysurveyor/', views.getissuebysurveyor),

    path('getsurveybyprovinsiai/', views.getsurveybyprovinsiai),
    path('getsurveybyprovinsibts/', views.getsurveybyprovinsibts),

    path('addHasilSurvey/relokasi/', views.PosthasilSurveyRelokasi),
    path('addhasilsurveybts/relokasi/', views.postBTSRelokasi),

    path('getsurveylogai/', views.getsurveylogai),
    path('getsurveylogbts/', views.getsurveylogbts),

    path('getsurveyorsubmitai/', views.getsurveyorsubmitai),
    path('getsurveyorsubmitbts/', views.getsurveyorsubmitbts),

    path('getpenugasan/count/surveyor/', views.countPenugasanSurveyor),

    path('getsurveyorlogai/', views.getsurveyorlogai),
    path('getsurveyorlogbts/', views.getsurveyorlogbts),

    path('getlaporan/', views.getLaporan),
    # path('addhasilsurveybts/',views.PostHasilSurveyBTS),
]
