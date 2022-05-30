from django.contrib import admin
from .models import BotUser
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(BotUser)
class BotUserModel(admin.ModelAdmin):
    list_display_links = ("tg_id", 'full_name', 'phone', 'is_active')
    list_display = list_display_links
    readonly_fields = list_display_links
    search_fields = ('full_name', 'phone')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
