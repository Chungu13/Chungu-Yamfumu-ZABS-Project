from django.contrib import admin
from zabs_project.admin_site import admin_site
from .models import CertificationApplication, ProductDetails, Document, Certification
from django.utils.html import format_html
from django.conf import settings
import os


class CertificationApplicationAdmin(admin.ModelAdmin):
    
   
    list_display = (
        'id',
        'manufacturer',
        'status',
        'quality_mark',
        'certified_local_supplier',
        'good_food_logo',
        'has_target_assessment_date',
        'target_assessment_date',
    )
    
   
    list_filter = (
        'status',
        'quality_mark',
        'certified_local_supplier',
        'good_food_logo',
    )
    
    
    search_fields = (
        'manufacturer__manufacturer__username', 
        'manufacturer__company_name',
        'status',
    )
    
    
    fields = (
        'manufacturer',
        'quality_mark',
        'certified_local_supplier',
        'good_food_logo',
        'has_target_assessment_date',
        'target_assessment_date',
        'status',
        'review_comment',
        'rejection_reason',
       )
    
    


class ProductDetailsAdmin(admin.ModelAdmin):
    
    list_display = ('id','certification_application', 'product_name','description', 'brand_or_trade_name', 'supporting_documents','standard', 
                    'annual_production_quantity', 'unit_selling_price')
    search_fields = ('product_name', 'brand_or_trade_name', 'certification_application__user_profile__company_name')
    list_filter = ('standard',)
   
   
    
    
class CertificationAdmin(admin.ModelAdmin):
    
    list_display = ('id','certification_application', 'custom_certification_id', 'manufacturer', 'product','first_issued','last_issued', 'expiry_date','authorized_signature','status','qr_code_link', 'pdf_file')
    search_fields = ('id', 'manufacturer__user__username')
    list_filter = ('status', 'first_issued', 'expiry_date')
    
    
    fieldsets = (
        (None, {'fields': ('certification_application','custom_certification_id', 'manufacturer', 'product', 'first_issued', 'last_issued', 
                           'expiry_date', 'authorized_signature' 'status')}), )
    date_hierarchy = 'first_issued'
    readonly_fields = ('custom_certification_id','qr_code_link',) 
    

    def qr_code_link(self, obj):
        if obj.qr_code:
            return format_html('<a href="{}" target="_blank">QR Code</a>', obj.qr_code.url)
        return "No QR code available"

    qr_code_link.short_description = 'QR Code'
    
    
    

class DocumentAdmin(admin.ModelAdmin):
   
    list_display = (
        'certification_application',
        'file',
        'file_name',
        'upload_date',
    )
    
 
    search_fields = (
        'file_name',
    )
    
   
    fields = (
        'certification_application',
        'file',
        'file_name',
    )
    
    
admin_site.register(CertificationApplication, CertificationApplicationAdmin)
admin_site.register(ProductDetails, ProductDetailsAdmin)
admin_site.register(Certification, CertificationAdmin)
admin_site.register(Document, DocumentAdmin)



