from django.db import models
from apps.users.models import UserProfile
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
import os
from django.conf import settings
from django.utils import timezone
from django.utils.html import format_html



class CertificationApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewing', 'Reviewing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    manufacturer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='certification_application')
    quality_mark = models.BooleanField(default=False)
    certified_local_supplier = models.BooleanField(default=False)
    good_food_logo = models.BooleanField(default=False)
    has_target_assessment_date = models.BooleanField(default=False, help_text="Do you have a target assessment date?")
    target_assessment_date = models.DateField(null=True, blank=True, help_text="If yes, please indicate the date.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    review_comment = models.TextField(blank=True, null=True)  
    rejection_reason = models.TextField(blank=True, null=True)  
    
    
    
 #---------------------------------------------------------------------------------------------------------------------------   
    def save(self, *args, **kwargs):
        if self.pk:
             old_status = CertificationApplication.objects.get(pk=self.pk).status
             if old_status != self.status and self.status == 'rejected':
                 if not self.rejection_reason:  
                      raise ValueError("Rejection reason must be provided when rejecting an application.")
        super().save(*args, **kwargs)
                     
             
             
               
#------------------------------------------------------------------------------------------------------------------------
# Document Model  

class Document(models.Model):
    certification_application = models.OneToOneField(CertificationApplication, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='certification_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.certification_application:
            return f"Document for Certification Application ID: {self.certification_application.pk}"
        return "Document with no related Certification Application"
    
    
#------------------------------------------------------------------------------------------------------------------------
# Product Details  Model      

class ProductDetails(models.Model):
    
    certification_application = models.OneToOneField(CertificationApplication,on_delete=models.CASCADE,related_name='product_details')
    product_name = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, help_text="Description of Product", default='')
    brand_or_trade_name = models.CharField(max_length=255, help_text="Brand or Trade Name", default='')
    standard = models.CharField(max_length=255, help_text="Standard", default='')
    supporting_documents = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='documents', null=True, blank=True) 
    annual_production_quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Annual Production Quantity", default=0.00)
    unit_selling_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit Selling Price (ZMW)", default=0.00)
        
    def __str__(self):
        return self.product_name
   
   
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Certification(models.Model):
    certification_application = models.OneToOneField(CertificationApplication,on_delete=models.CASCADE,related_name='certification')
    custom_certification_id = models.CharField(max_length=255, unique=True, blank=True, editable=False)
    manufacturer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductDetails, on_delete=models.CASCADE, related_name='certifications')
    first_issued = models.DateField(default=timezone.now, blank=False, null=True)
    last_issued = models.DateField(default=timezone.now, blank=False, null=True)
    modified_on = models.DateField(default=timezone.now, blank=False, null=False)
    expiry_date = models.DateField(default=timezone.now, blank=False, null=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)
    status = models.CharField(max_length=50, default='Approved')
    
    
    
    def generate_qr_code(self):
        # Generate URL pointing to the GraphQL API
        qr_url = f"http://localhost:8000/graphql?query={{certification(id:\"{self.id}\"){{certificationId manufacturer{{companyname}} firstIssued expiryDate status product{{productId productName description}}}}}}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_url)
        qr.make(fit=True)

        # Save the QR code image
        qr_img = qr.make_image(fill='black', back_color='white')
        qr_file_name = f'qr_code_{self.id}.png'
        qr_file_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', qr_file_name)

        os.makedirs(os.path.dirname(qr_file_path), exist_ok=True)
        qr_img.save(qr_file_path)

        self.qr_code = f'qr_codes/{qr_file_name}'
      
        
        
     
    # Generate Custom Certification ID
    def generate_custom_certification_id(self):
        prefix = 'CRT'
        separator = '-'

        last_entry = Certification.objects.order_by('-id').first()
        if last_entry and last_entry.custom_certification_id:
            
            numeric_part = last_entry.custom_certification_id.replace(separator, '').replace(prefix, '')
            new_number = int(numeric_part) + 1
        else:
            new_number = 1

        formatted_number = f'{new_number:08}'
        new_custom_certification_id = f'{formatted_number[:3]}{separator}{formatted_number[3:5]}{separator}{formatted_number[5:]}{separator}{prefix}'

        return new_custom_certification_id
    
        
    def save(self, *args, **kwargs):
  
        super().save(*args, **kwargs)
    
        if not self.custom_certification_id:
            self.custom_certification_id = self.generate_custom_certification_id()
       
        super().save(update_fields=['custom_certification_id'])

        if not self.qr_code:
            self.generate_qr_code()

        super().save(update_fields=['qr_code'])

    
    
    
    
    

    

    
        
        






             
