from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="login/password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="login/password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="login/password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="login/password_reset_done.html"),
         name="password_reset_complete"),
]
