# # utils/validators.py
# from zabs_project.apps.users.models import UserProfile
# from django.core.exceptions import ValidationError

# def validate_profile_exists(profile_id):
#     try:
#         return UserProfile.objects.get(pk=profile_id)
#     except UserProfile.DoesNotExist:
#         raise ValidationError("Profile not found.")
