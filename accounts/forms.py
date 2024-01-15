from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm,
                                       AuthenticationForm)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, PasswordInput

from blog import forms


class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field_name in ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Такой E-mail уже существует!')
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = None


class CustomPasswordResetForm(PasswordResetForm):
    pass


class CustomSetPasswordForm(SetPasswordForm):
    pass


class UserProfileEditForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        for field_name in ['username', 'email', 'first_name', 'last_name']:
            self.fields[field_name].help_text = None
