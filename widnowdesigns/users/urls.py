from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('password-reset/', PasswordResetView.as_view(template_name="users/password_reset_form.html",
                                                      email_template_name="users/password_reset_email.html",
                                                      success_url=reverse_lazy("users:password_reset_done")), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),

    path('password-reset/<uidb64>/<token>', PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html",
                                                                             success_url=reverse_lazy("users:password_reset_complete")), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),

    path('registration/', views.registration, name='registration'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]