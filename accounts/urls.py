from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from accounts.forms import CustomPasswordChangeForm
from accounts.views import CustomRegistrationView, CustomLoginView, CustomPasswordResetView, \
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView, UserProfileView, EditProfileView, \
    CustomPasswordResetDoneView, ProfileFollowingView
from accounts.views import logout_view

app_name = 'accounts'

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", CustomRegistrationView.as_view(), name="signup"),
    path("logout/", logout_view, name='logout'),
    path("password_change/", PasswordChangeView.as_view(
        template_name='accounts/registration/password_change.html',
        form_class=CustomPasswordChangeForm,
        success_url=reverse_lazy('accounts:password-change-done')
    ), name="password-change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(
        template_name='accounts/registration/password_change_done.html',
    ), name="password-change-done"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password-reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password-reset-done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(), name="password-reset-complete"),
    path("<slug:slug>/", UserProfileView.as_view(), name="profile"),
    path("<str:slug>/update/", EditProfileView.as_view(), name="edit-profile"),
    path("<str:slug>/follow/", ProfileFollowingView.as_view(), name="follow"),
]
