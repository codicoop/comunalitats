from django.contrib.auth.views import LogoutView, PasswordChangeDoneView
from django.urls import path
from apps.cc_users import views
from django.contrib.auth.decorators import login_required

from apps.cc_users.decorators import anonymous_required
from apps.cc_users.views import (
    PasswordResetView, PasswordResetConfirmView,
    PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView
)
from apps.coopolis.views import LoginSignupContainerView, CoopolisLoginView, \
    CoopolisSignUpView

urlpatterns = [
    path('users/loginsignup/', anonymous_required(
        LoginSignupContainerView.as_view()), name='loginsignup'),
    path('users/login_post/', anonymous_required(
        CoopolisLoginView.as_view()), name='login_post'),
    path('users/login/', anonymous_required(
        CoopolisLoginView.as_view()), name='login'),
    path('users/signup_post', anonymous_required(
        CoopolisSignUpView.as_view()), name='signup_post'),
    path('users/signup', anonymous_required(
        CoopolisSignUpView.as_view()), name='signup'),


    path('logout/', LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        PasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(),
        name='password_change_done')
    ,
    path(
        'users/profile/',
        login_required(views.MyAccountView.as_view()),
        name='user_profile'
    ),
    path("compte/reiniciar_contrasenya/", PasswordResetView.as_view(),
         name="password_reset"),
    path(
        "account/password_reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "compte/reiniciar/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "account/reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
