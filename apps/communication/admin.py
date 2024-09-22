from django.contrib import admin
from zabs_project.admin_site import admin_site
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')
    search_fields = ('sender__user__username', 'content')
    list_filter = ('recipient', 'timestamp')
    readonly_fields = ('timestamp',)  # Timestamp is auto-generated

admin_site.register(Message, MessageAdmin)
