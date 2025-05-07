from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentID

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'department')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentID)