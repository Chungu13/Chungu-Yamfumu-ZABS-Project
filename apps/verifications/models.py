from django.db import models
from apps.certifications.models import Certification
from apps.users.models import UserProfile,CustomUser
from django.utils import timezone

class Verification(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE)
    verified_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verifications' , limit_choices_to={'user_type': 'consumer'})
    verification_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Verification of {self.certification} by {self.verified_by.username}"

# verified_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='verifications', limit_choices_to={'user_type': 'consumer'})

class Feedback(models.Model): 
    consumer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback', limit_choices_to={'user_type': 'consumer'})
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
      
    