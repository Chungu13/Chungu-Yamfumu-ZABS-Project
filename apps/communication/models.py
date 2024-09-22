from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone


# Defined a new class for the communication between the manufacturer and zabs
# Defined fields for it.
# created relationships between the userprofile and sender (one to many)
# one userprofile can send many messages. 
# one recipient can recieve many messages.
 
class Message(models.Model):
   
    sender = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE, limit_choices_to={'user_type': 'manufacturer'})
    recipient = models.ForeignKey(CustomUser, related_name='received_messages', on_delete=models.CASCADE, limit_choices_to={'user_type': 'admin'})
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
