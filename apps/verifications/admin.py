from django.contrib import admin
from zabs_project.admin_site import admin_site
from .models import Verification, Feedback

class VerificationAdmin(admin.ModelAdmin):
    list_display = ('certification', 'verified_by', 'verification_date', 'status')
    list_filter = ('status', 'verification_date')
    search_fields = ('certification__product_name', 'verified_by__user__username')



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('consumer', 'content', 'timestamp')  # Fields to display in the admin list view
    search_fields = ('user_profile__user__username', 'content')  # Fields that can be searched in the admin interface
    list_filter = ('timestamp',)  # Filter by timestamp in the admin interface


admin_site.register(Feedback, FeedbackAdmin)
admin_site.register(Verification, VerificationAdmin)
