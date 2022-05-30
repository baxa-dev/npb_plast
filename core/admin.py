from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone')
    list_display_links = list_display
    search_fields = ('full_name', 'phone')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
