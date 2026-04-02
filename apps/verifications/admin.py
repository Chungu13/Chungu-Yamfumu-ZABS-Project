from django.contrib import admin
from zabs_project.admin_site import admin_site
from .models import Verification, Feedback

class VerificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'certification', 'verification_date', 'status')     
    list_filter = ('status', 'verification_date')
    search_fields = ('certification__product_name',)



class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('consumer', 'content', 'timestamp')  
    search_fields = ('user_profile__user__username', 'content') 
    list_filter = ('timestamp',)  


admin_site.register(Feedback, FeedbackAdmin)
admin_site.register(Verification, VerificationAdmin)
