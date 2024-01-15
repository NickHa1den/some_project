from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from accounts.forms import CustomUserRegistrationForm, CustomPasswordResetForm, \
    CustomSetPasswordForm, CustomLoginForm, UserProfileEditForm
from accounts.models import Profile


class UserProfileView(TemplateView):
    template_name = 'accounts/profile.html'


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/registration/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('blog:home')


class CustomRegistrationView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/registration/signup.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('accounts:login')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/registration/password_reset_form.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password-reset-complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'


def logout_view(request):
    logout(request)
    return redirect('/')


class EditProfileView(UpdateView):
    model = get_user_model()
    template_name = 'accounts/edit_profile.html'
    form_class = UserProfileEditForm
    success_url = reverse_lazy('accounts:profile')
