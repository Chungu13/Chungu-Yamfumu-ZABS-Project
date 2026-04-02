import graphene
import re
from .types import CustomUserType, UserProfileType
from apps.users.models import CustomUser, UserProfile

class CreateCustomUser(graphene.Mutation):
    user = graphene.Field(CustomUserType)
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirmation = graphene.String(required=True)
        user_type = graphene.String(required=True)
        location = graphene.String()
        gender = graphene.String()
        date_of_birth = graphene.Date()
        profile_picture = graphene.String()

    def mutate(self, info, username, email, phone_number, password, password_confirmation, user_type, **kwargs):
        if password != password_confirmation:
            raise Exception("Passwords do not match")
        user = CustomUser(username=username, email=email, phone_number=phone_number, user_type=user_type, **kwargs)
        user.set_password(password)
        user.save()
        return CreateCustomUser(user=user)

class UpdateCustomUser(graphene.Mutation):
    user = graphene.Field(CustomUserType)
    class Arguments:
        user_id = graphene.ID(required=True)
        username = graphene.String()
        email = graphene.String()
        phone_number = graphene.String()
        location = graphene.String()
        user_type = graphene.String()
        gender = graphene.String()
        profile_picture = graphene.String()

    def mutate(self, info, user_id, **kwargs):
        user = CustomUser.objects.get(pk=user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return UpdateCustomUser(user=user)

class DeleteCustomUser(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        user_id = graphene.ID(required=True)
    def mutate(self, info, user_id):
        user = CustomUser.objects.get(pk=user_id)
        user.delete()
        return DeleteCustomUser(success=True)

class CreateUserProfile(graphene.Mutation):
    profile = graphene.Field(UserProfileType)
    class Arguments:
        user_id = graphene.ID(required=True)
        company_name = graphene.String(required=True)
        contact_person = graphene.String(required=True)
        physical_address = graphene.String(required=True)
        position = graphene.String(required=True)
        mobile = graphene.String(required=True)
        email = graphene.String(required=True)
        postal_address = graphene.String()
        website = graphene.String()

    def mutate(self, info, user_id, mobile, **kwargs):
        if not re.match(r'^\+260\d{9}$', mobile):
            raise Exception("Mobile number must follow the format: +260XXXXXXXXX")
        user = CustomUser.objects.get(pk=user_id)
        profile = UserProfile.objects.create(user=user, mobile=mobile, **kwargs)
        return CreateUserProfile(profile=profile)

class UpdateUserProfile(graphene.Mutation):
    profile = graphene.Field(UserProfileType)
    class Arguments:
        profile_id = graphene.ID(required=True)
        company_name = graphene.String()
        contact_person = graphene.String()
        physical_address = graphene.String()
        position = graphene.String()
        mobile = graphene.String()
        email = graphene.String()
        postal_address = graphene.String()
        website = graphene.String()

    def mutate(self, info, profile_id, **kwargs):
        profile = UserProfile.objects.get(pk=profile_id)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        profile.save()
        return UpdateUserProfile(profile=profile)

class DeleteUserProfile(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        profile_id = graphene.ID(required=True)
    def mutate(self, info, profile_id):
        profile = UserProfile.objects.get(pk=profile_id)
        profile.delete()
        return DeleteUserProfile(success=True)

class Mutation(graphene.ObjectType):
    create_custom_user = CreateCustomUser.Field()
    update_custom_user = UpdateCustomUser.Field()
    delete_custom_user = DeleteCustomUser.Field()
    create_user_profile = CreateUserProfile.Field()
    update_user_profile = UpdateUserProfile.Field()
    delete_user_profile = DeleteUserProfile.Field()
