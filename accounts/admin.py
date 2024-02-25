from django.contrib import admin

from accounts.models import Profile, EmailVerification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'slug')


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ['code', 'user', 'expiration', 'created']
    readonly_fields = ['created']
