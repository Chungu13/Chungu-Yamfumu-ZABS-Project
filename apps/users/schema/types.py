import graphene
from graphene_django.types import DjangoObjectType
from apps.users.models import CustomUser, UserProfile

class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "phone_number", "location", "user_type", "gender", "date_of_birth", "profile_picture")

class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ('id', 'company_name', 'physical_address', 'postal_address', 'contact_person', 'mobile',  'position', 'email', 'website')
