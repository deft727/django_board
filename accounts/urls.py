from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views as accounts_views


urlpatterns = [
        path('signup/',ChooseSignup.as_view(), name='signup'),
        path('signup-reader/',RegistrationViewReader.as_view(), name='signup_reader'),
                path('signup-bloger/',RegistrationViewBloger.as_view(), name='signup_bloger'),
        path('logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                path('reset/', auth_views.PasswordResetView.as_view(template_name="password-reset.html"),name="password_reset"),
                path('reset/done/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
                path('passwod/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
                path('reset/complete/',  auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete"),
        path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
        path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
        path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),

]