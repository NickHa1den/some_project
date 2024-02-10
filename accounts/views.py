from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.sites.models import Site
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from accounts.forms import CustomUserRegistrationForm, CustomPasswordResetForm, \
    CustomSetPasswordForm, CustomLoginForm, UserProfileEditForm
from accounts.models import Profile
from blog.models import Post
from blog.utils import TagMixin


class UserProfileView(TagMixin, ListView):
    model = Profile
    template_name = 'accounts/profile.html'
    paginate_by = 2

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['slug'])

    def get_queryset(self):
        user = self.get_object()
        queryset = Post.objects.filter(author__username=user).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'REAL BLOG! | Профиль'
        context['user_posts'] = self.get_queryset()
        context['user_page'] = self.get_object()
        return context


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/registration/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('blog:home')

    def form_invalid(self, form):
        messages.error(self.request, 'Введите правильные данные. Поля формы могу быть чувствительны к регистру.')
        return super().form_invalid(form)


class CustomRegistrationView(CreateView):
    form_class = CustomUserRegistrationForm
    template_name = 'accounts/registration/signup.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        messages.success(self.request, 'Регистрация прошла успешно. Авторизуйтесь на сайт с Вашими данными.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/registration/password_reset_form.html'
    success_url = reverse_lazy('accounts:password-reset-done')
    email_template_name = 'accounts/registration/password_reset_email.txt'
    html_email_template_name = 'accounts/registration/password_reset_email.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'
    success_url = reverse_lazy('accounts:password-reset-confirm')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')
        return context


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password-reset-complete')

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'


def logout_view(request):
    logout(request)
    return redirect('/')


class EditProfileView(UpdateView):
    model = get_user_model()
    form_class = UserProfileEditForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'REAL BLOG! | Редактирование профиля'
        if self.request.POST:
            context['form'] = UserProfileEditForm(
                self.request.POST,
                self.request.FILES,
                instance=self.request.user
            )
        else:
            context['form'] = UserProfileEditForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
                messages.success(self.request, 'Данные профиля обновлены')
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.non_field_errors())
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'slug': self.request.user})

# @method_decorator(login_required, name='dispatch')
# class ProfileFollowingView(View):
#     model = Profile
#
#     def is_ajax(self):
#         return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'
#
#     def post(self, request, username):

