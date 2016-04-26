from django.contrib import admin
from models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserProfile(admin.StackedInline):
    model = UserProfile
    extra = 0 

class UserAddProfile(UserAdmin):
    inlines = [UserProfile,]
    
admin.site.unregister(User)
admin.site.register(User,UserAddProfile )