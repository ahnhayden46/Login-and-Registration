from django.urls import path
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
    path(
        r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate')
]
