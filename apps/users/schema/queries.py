import graphene
from apps.users.models import CustomUser, UserProfile
from .types import CustomUserType, UserProfileType

class Query(graphene.ObjectType):
    all_custom_users = graphene.List(CustomUserType)
    all_user_profiles = graphene.List(UserProfileType)
    custom_user = graphene.Field(CustomUserType, id=graphene.ID(required=True))
    user_profile = graphene.Field(UserProfileType, id=graphene.ID(required=True))

    def resolve_all_custom_users(self, info):
        return CustomUser.objects.all()
    
    def resolve_all_user_profiles(self, info):
        return UserProfile.objects.all()

    def resolve_custom_user(self, info, id):
        return CustomUser.objects.get(pk=id)
    
    def resolve_user_profile(self, info, id):
        return UserProfile.objects.get(pk=id)
