from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.evaluationRequests),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('evaluation_requests/', views.evaluationRequests,
         name='evaluation-requests'),
    path('request_evaluation/', views.requestEvaluation,
         name='request-evaluation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('authenticate_login/<uidb64>/<token>/',
         views.authenticate_login, name='authenticate_login'),
    # url(
    #     r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    # url(
    #     r'^authenticate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.authenticate, name='authenticate'),
]
