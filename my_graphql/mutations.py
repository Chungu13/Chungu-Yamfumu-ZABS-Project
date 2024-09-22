import graphene
from .types import CertificationApplicationType, DocumentType, ProductDetailsType, CertificationType, UserProfileType
from .types import MessageType, VerificationType, FeedbackType, CustomUserType
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from apps.users.models import CustomUser, UserProfile
from apps.communication.models import Message
from apps.verifications.models import Verification, Feedback
import uuid
from django.utils import timezone



class CreateCustomUser(graphene.Mutation):
    # This defines what will be returned 
    user = graphene.Field(CustomUserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        phone_number = graphene.String(required=True)
        password = graphene.String(required = True)
        password_confirmation = graphene.String(required=True)
        user_type = graphene.String(required=True)
        location = graphene.String()
        gender = graphene.String()
        date_of_birth = graphene.Date()
        profile_picture = graphene.String()
    

    def mutate(self, info, username, email, phone_number, password, password_confirmation):
        if password != password_confirmation:
            raise Exception("Passwords do not match")

        user = CustomUser(
            username=username,
            email=email,
            phone_number=phone_number
        )
        user.set_password(password)  # Encrypts the password
        user.save()

        return CreateCustomUser(user=user, success=True)
    
    





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
        date_of_birth = graphene.Date()
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



# ----- UserProfile -----

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

    def mutate(self, info, user_id, **kwargs):
        user = CustomUser.objects.get(pk=user_id)
        profile = UserProfile(user=user, **kwargs)
        profile.save()
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




# ----- CertificationApplication -----
class CreateCertificationApplication(graphene.Mutation):
    certification_application = graphene.Field(CertificationApplicationType)

    class Arguments:
        manufacturer_id = graphene.ID()
        quality_mark = graphene.Boolean()
        certified_local_supplier = graphene.Boolean()
        good_food_logo = graphene.Boolean()
        has_target_assessment_date = graphene.Boolean()
        target_assessment_date = graphene.Date()
        status = graphene.String() 
        review_comment = graphene.String()
        rejection_reason = graphene.String()

    def mutate(self, info, manufacturer_id, **kwargs):
        manufacturer = CustomUser.objects.get(pk=manufacturer_id)
        certification_application = CertificationApplication.objects.create(
            manufacturer=manufacturer, **kwargs
        )
        return CreateCertificationApplication(certification_application=certification_application)
    

class UpdateCertificationApplication(graphene.Mutation):
    certification_application = graphene.Field(CertificationApplicationType)

    class Arguments:
        certification_application_id = graphene.ID(required=True)
        quality_mark = graphene.Boolean()
        certified_local_supplier = graphene.Boolean()
        good_food_logo = graphene.Boolean()
        has_target_assessment_date = graphene.Boolean()
        target_assessment_date = graphene.Date()
        status = graphene.String() 
        review_comment = graphene.String()
        rejection_reason = graphene.String()


    def mutate(self, info, certification_application_id, **kwargs):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        for key, value in kwargs.items():
            setattr(certification_application, key, value)
        certification_application.save()
        return UpdateCertificationApplication(certification_application=certification_application)


class DeleteCertificationApplication(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        certification_application_id = graphene.ID(required=True)

    def mutate(self, info, certification_application_id):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        certification_application.delete()
        return DeleteCertificationApplication(success=True)
    
    
    

# ----- ProductDetails -----
class CreateProductDetails(graphene.Mutation):
    product_details = graphene.Field(ProductDetailsType)

    class Arguments:
        certification_application_id = graphene.ID()
        product_name = graphene.String()
        description = graphene.String()
        brand_or_trade_name = graphene.String()
        standard = graphene.String()
        supporting_documents_id = graphene.ID()
        annual_production_quantity = graphene.Float()
        unit_selling_price = graphene.Float()

    def mutate(self, info, certification_application_id, supporting_documents_id, **kwargs):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        supporting_documents = Document.objects.get(pk=supporting_documents_id)
        product_details = ProductDetails.objects.create(
            certification_application=certification_application,
            supporting_documents=supporting_documents,
            **kwargs
        )
        return CreateProductDetails(product_details=product_details)
    

class UpdateProductDetails(graphene.Mutation):
    product_details = graphene.Field(ProductDetailsType)

    class Arguments:
        product_details_id = graphene.ID(required=True)
        product_name = graphene.String()
        description = graphene.String()
        brand_or_trade_name = graphene.String()
        standard = graphene.String()
        annual_production_quantity = graphene.Float()
        unit_selling_price = graphene.Float()

    def mutate(self, info, product_details_id, **kwargs):
        product_details = ProductDetails.objects.get(pk=product_details_id)
        for key, value in kwargs.items():
            setattr(product_details, key, value)
        product_details.save()
        return UpdateProductDetails(product_details=product_details)
    

class DeleteProductDetails(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        product_details_id = graphene.ID(required=True)

    def mutate(self, info, product_details_id):
        product_details = ProductDetails.objects.get(pk=product_details_id)
        product_details.delete()
        return DeleteProductDetails(success=True)
    
    
    
    

# ----- Document -----
class CreateDocument(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        certification_application_id = graphene.ID()
        file = graphene.String() 
        file_name = graphene.String()

    def mutate(self, info, certification_application_id, **kwargs):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        document = Document.objects.create(certification_application=certification_application, **kwargs)
        return CreateDocument(document=document)


class UpdateDocument(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        document_id = graphene.ID(required=True)
        file = graphene.String()
        file_name = graphene.String()

    def mutate(self, info, document_id, **kwargs):
        document = Document.objects.get(pk=document_id)
        for key, value in kwargs.items():
            setattr(document, key, value)
        document.save()
        return UpdateDocument(document=document)


class DeleteDocument(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        document_id = graphene.ID(required=True)

    def mutate(self, info, document_id):
        document = Document.objects.get(pk=document_id)
        document.delete()
        return DeleteDocument(success=True)
    


# Mutation class to create a new Certification
class CreateCertification(graphene.Mutation):
    certification = graphene.Field(CertificationType)

    class Arguments:
        certification_application_id = graphene.ID(required=True)
        manufacturer_id = graphene.ID(required=True)
        first_issued = graphene.Date(required=False)
        last_issued = graphene.Date(required=False)
        modified_on = graphene.Date(required=False)
        expiry_date = graphene.Date(required=True)
        status = graphene.String(required=False)

    def mutate(self, info, certification_application_id, manufacturer_id, **kwargs):
        # Get the CertificationApplication and Manufacturer (UserProfile)
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        manufacturer = UserProfile.objects.get(pk=manufacturer_id)

        # Auto-generate a unique certification ID
        certification_id = str(uuid.uuid4())  # renamed the variable to avoid confusion

        # Set the optional fields with defaults if not provided
        first_issued = kwargs.get('first_issued', timezone.now().date())
        last_issued = kwargs.get('last_issued', timezone.now().date())
        modified_on = kwargs.get('modified_on', timezone.now().date())
        status = kwargs.get('status', 'Approved')

        # Create the Certification object
        certification = Certification.objects.create(
            certification_application=certification_application,
            manufacturer=manufacturer,
            certification_id=certification_id,  # Passing the generated ID
            first_issued=first_issued,
            last_issued=last_issued,
            modified_on=modified_on,
            expiry_date=kwargs.get('expiry_date'),
            status=status
        )

        return CreateCertification(certification=certification)


    
    

# # ----- Certification -----
# class CreateCertification(graphene.Mutation):
#     certification = graphene.Field(CertificationType)

#     class Arguments:
#         certification_application_id = graphene.ID()
#         custom_certification_id = graphene.ID()
#         manufacturer_id = graphene.ID()
#         first_issued = graphene.Date()
#         last_issued = graphene.Date()
#         modified_on = graphene.Date()
#         expiry_date = graphene.Date()
#         qr_code = graphene.String()  
#         status = graphene.String()

#     def mutate(self, info, certification_application_id, custom_certification_id, manufacturer_id, **kwargs):
#         certification_application = CertificationApplication.objects.get(pk=certification_application_id)
#         manufacturer = UserProfile.objects.get(pk=manufacturer_id)
        
#         certification_id = str(uuid.uuid4())  # renamed the variable to avoid confusion
        
#         certification = Certification.objects.create(
#             certification_application=certification_application,
#             manufacturer=manufacturer,
#             **kwargs
#         )
#         return CreateCertification(certification=certification)


class DeleteCertification(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        certification_id = graphene.ID(required=True)

    def mutate(self, info, certification_id):
        certification = Certification.objects.get(pk=certification_id)
        certification.delete()
        return DeleteCertification(success=True)




# ----- Message -----
class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        sender_id = graphene.ID(required=True)
        recipient_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_id, recipient_id, content):
        sender = CustomUser.objects.get(pk=sender_id)
        recipient = CustomUser.objects.get(pk=recipient_id)
        message = Message.objects.create(sender=sender, recipient=recipient, content=content)
        return CreateMessage(message=message)

class UpdateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        message_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, message_id, **kwargs):
        message = Message.objects.get(pk=message_id)
        for key, value in kwargs.items():
            setattr(message, key, value)
        message.save()
        return UpdateMessage(message=message)

class DeleteMessage(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        message_id = graphene.ID(required=True)

    def mutate(self, info, message_id):
        message = Message.objects.get(pk=message_id)
        message.delete()
        return DeleteMessage(success=True)



# ----- Feedback -----
class CreateFeedback(graphene.Mutation):
    feedback = graphene.Field(FeedbackType)

    class Arguments:
        user_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, user_id, content):
        user = CustomUser.objects.get(pk=user_id)
        feedback = Feedback.objects.create(user=user, content=content)
        return CreateFeedback(feedback=feedback)



class UpdateFeedback(graphene.Mutation):
    feedback = graphene.Field(FeedbackType)

    class Arguments:
        feedback_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, feedback_id, **kwargs):
        feedback = Feedback.objects.get(pk=feedback_id)
        for key, value in kwargs.items():
            setattr(feedback, key, value)
        feedback.save()
        return UpdateFeedback(feedback=feedback)



class DeleteFeedback(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        feedback_id = graphene.ID(required=True)

    def mutate(self, info, feedback_id):
        feedback = Feedback.objects.get(pk=feedback_id)
        feedback.delete()
        return DeleteFeedback(success=True)
    



# ----- Verification -----
class CreateVerification(graphene.Mutation):
    verification = graphene.Field(VerificationType)

    class Arguments:
        user_id = graphene.ID(required=True)
        qr_code = graphene.String(required=True)
        verification_status = graphene.String()

    def mutate(self, info, user_id, **kwargs):
        user = CustomUser.objects.get(pk=user_id)
        verification = Verification.objects.create(user=user, **kwargs)
        return CreateVerification(verification=verification)


class UpdateVerification(graphene.Mutation):
    verification = graphene.Field(VerificationType)

    class Arguments:
        verification_id = graphene.ID(required=True)
        qr_code = graphene.String()
        verification_status = graphene.String()

    def mutate(self, info, verification_id, **kwargs):
        verification = Verification.objects.get(pk=verification_id)
        for key, value in kwargs.items():
            setattr(verification, key, value)
        verification.save()
        return UpdateVerification(verification=verification)


class DeleteVerification(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        verification_id = graphene.ID(required=True)

    def mutate(self, info, verification_id):
        verification = Verification.objects.get(pk=verification_id)
        verification.delete()
        return DeleteVerification(success=True)

 
    
# Mutation class
class Mutation(graphene.ObjectType):
    
    create_custom_user = CreateCustomUser.Field()
    update_custom_user = UpdateCustomUser.Field()
    delete_custom_user = DeleteCustomUser.Field()

    create_user_profile = CreateUserProfile.Field()
    update_user_profile = UpdateUserProfile.Field()
    delete_user_profile = DeleteUserProfile.Field()

    create_certification_application = CreateCertificationApplication.Field()
    update_certification_application = UpdateCertificationApplication.Field()
    delete_certification_application = DeleteCertificationApplication.Field()

    create_product_details = CreateProductDetails.Field()
    update_product_details = UpdateProductDetails.Field()
    delete_product_details = DeleteProductDetails.Field()

    create_document = CreateDocument.Field()
    update_document = UpdateDocument.Field()
    delete_document = DeleteDocument.Field()

    create_certification = CreateCertification.Field()
    delete_certification = DeleteCertification.Field()

    create_message = CreateMessage.Field()
    update_message = UpdateMessage.Field()
    delete_message = DeleteMessage.Field()

    create_verification = CreateVerification.Field()
    update_verification = UpdateVerification.Field()
    delete_verification = DeleteVerification.Field()

    create_feedback = CreateFeedback.Field()
    update_feedback = UpdateFeedback.Field()
    delete_feedback = DeleteFeedback.Field()    
    
    