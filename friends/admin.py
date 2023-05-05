from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from friends.models import User, FriendRequest


class MyUserAdmin(UserAdmin):
    list_display = ('username',)
    list_display_links = ('username',)
    search_fields = ('username',)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient',)
    list_display_links = ('sender', 'recipient',)
    search_fields = ('sender', 'recipient',)


admin.site.register(User, UserAdmin)
admin.site.register(FriendRequest, RequestAdmin)
