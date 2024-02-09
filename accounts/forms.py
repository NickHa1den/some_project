from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm,
                                       AuthenticationForm)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from accounts.models import Profile


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Введите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control py-2'


class CustomUserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Введите email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'
        for field_name in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Такой E-mail уже существует!')
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите старый пароль'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите новый пароль'}))

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = None


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control py-2'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Введите Ваш адрес электронной почты'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователя с email: {email} не существует')
        return cleaned_data


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Подтвердите новый пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'
        for field_name in ['new_password1', 'new_password2']:
            self.fields[field_name].help_text = None


class UserProfileEditForm(ModelForm):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field_name in ['username', 'email', 'first_name', 'last_name']:
            self.fields[field_name].help_text = None
