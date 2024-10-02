import graphene
from .types import CertificationApplicationType, DocumentType, ProductDetailsType,  UserProfileType, CertificationType
from .types import MessageType, VerificationType, FeedbackType, CustomUserType
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from apps.users.models import CustomUser, UserProfile
from apps.communication.models import Message
from apps.verifications.models import Verification, Feedback
from django.utils import timezone
from decimal import Decimal
from graphql import GraphQLError
import re


# ----- CustomUser -----

class CreateCustomUser(graphene.Mutation):
    
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
    

    def mutate(self, info, username, email, phone_number, password, password_confirmation, user_type):
        if password != password_confirmation:
            raise Exception("Passwords do not match")

        user = CustomUser(
            username=username,
            email=email,
            phone_number=phone_number,
            user_type = user_type,
        )
        user.set_password(password)  # Password Encryption 
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
        
         
        try:
           user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise Exception("User not found")


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

    def mutate(self, info, user_id,  mobile, **kwargs):
        
        
        # Validate mobile number format
        if not re.match(r'^\+260\d{9}$', mobile):
            raise Exception("Mobile number must follow the format: +260XXXXXXXXX")
        
        
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise Exception("User not found")
        
        
        profile = UserProfile.objects.create(
            user=user,
            mobile=mobile,  
            **kwargs
        )
        
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
        
        try:
           profile = UserProfile.objects.get(pk=profile_id)
        except UserProfile.DoesNotExist:
            raise Exception("User not found")
        
        for key, value in kwargs.items():
            setattr(profile, key, value)
            
        profile.save()
        return UpdateUserProfile(profile=profile)
    
    

class DeleteUserProfile(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        profile_id = graphene.ID(required=True)

    def mutate(self, info, profile_id):
        try:
           profile = UserProfile.objects.get(pk=profile_id)
        except UserProfile.DoesNotExist:
            raise Exception("User not found")
        
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
        
        try:
           manufacturer = UserProfile.objects.get(pk=manufacturer_id)
        except UserProfile.DoesNotExist:
            raise Exception("Manufacturer not found")
        
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
       
        try:
           certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise Exception("Certification Application not found")
        
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
        
        try:
           certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise Exception("Certification Application not found")
        
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
        supporting_documents_id = graphene.ID(required=False)
        annual_production_quantity = graphene.String()  
        unit_selling_price = graphene.String()  

    def mutate(self, info, certification_application_id, supporting_documents_id=None, **kwargs):
        
        try:
            certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise Exception("Certification application not found")

        
        supporting_documents = None
        if supporting_documents_id:
            try:
                supporting_documents = Document.objects.get(pk=supporting_documents_id)
            except Document.DoesNotExist:
                raise Exception(f"Document with ID {supporting_documents_id} does not exist")

       
        annual_production_quantity = Decimal(kwargs.get('annual_production_quantity'))
        unit_selling_price = Decimal(kwargs.get('unit_selling_price'))

        
        product_details = ProductDetails.objects.create(
            certification_application=certification_application,
            supporting_documents=supporting_documents,
            product_name=kwargs.get('product_name'),
            description=kwargs.get('description'),
            brand_or_trade_name=kwargs.get('brand_or_trade_name'),
            standard=kwargs.get('standard'),
            annual_production_quantity=annual_production_quantity,  # Use the converted value
            unit_selling_price=unit_selling_price,  # Use the converted value
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
        
        
        try:
           product_details = ProductDetails.objects.get(pk=product_details_id)
        except ProductDetails.DoesNotExist:
            raise Exception("Product Details not found")
        
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
        
        try:
           product_details = ProductDetails.objects.get(pk=product_details_id)
        except ProductDetails.DoesNotExist:
            raise Exception("Product Details not found")
        
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
        
        try:
          certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise Exception("Certification Application not found")
        
        
        document = Document.objects.create(certification_application=certification_application, **kwargs)
        return CreateDocument(document=document)




class UpdateDocument(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        document_id = graphene.ID(required=True)
        file = graphene.String()
        file_name = graphene.String()

    def mutate(self, info, document_id, **kwargs):
       
        try:
           document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            raise Exception("Document not found")
        
        for key, value in kwargs.items():
            setattr(document, key, value)
            
        document.save()
        return UpdateDocument(document=document)



class DeleteDocument(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        document_id = graphene.ID(required=True)

    def mutate(self, info, document_id):
        try:
           document = Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            raise Exception("Document not found")
        
        document.delete()
        return DeleteDocument(success=True)
    


# ----- Certification-----
class CreateCertification(graphene.Mutation):
    certification = graphene.Field(CertificationType)

    class Arguments:
        certification_application_id = graphene.ID(required=True)
        manufacturer_id = graphene.ID(required=True)
        product_id = graphene.ID(required=True)
        first_issued = graphene.Date(required=True)
        last_issued = graphene.Date(required=True)
        expiry_date = graphene.Date(required=True)

    def mutate(self, info, certification_application_id, manufacturer_id, product_id, first_issued, last_issued, expiry_date):
        
        try:
            certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise GraphQLError("Certification Application does not exist.")

        try:
            manufacturer = UserProfile.objects.get(pk=manufacturer_id)
        except UserProfile.DoesNotExist:
            raise GraphQLError("Manufacturer does not exist.")

        try:
            product = ProductDetails.objects.get(pk=product_id)
        except ProductDetails.DoesNotExist:
            raise GraphQLError("Product does not exist.")

        
        certification = Certification.objects.create(
            certification_application=certification_application,
            manufacturer=manufacturer,
            product=product,  
            first_issued=first_issued,
            last_issued=last_issued,
            expiry_date=expiry_date,
        )
        certification.save()

        return CreateCertification(certification=certification)


class DeleteCertification(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        certification_id = graphene.ID(required=True)

    def mutate(self, info, certification_id):
        try:
            # Attempt to find the certification
            certification = Certification.objects.get(pk=certification_id)
        except Certification.DoesNotExist:
            raise GraphQLError("Certification does not exist.")

        # Delete the certification
        certification.delete()

        # Return success response
        return DeleteCertification(success=True)



# ----- Message -----
class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        sender_id = graphene.ID(required=True)
        recipient_id = graphene.ID(required=True)
        content = graphene.String(required=True)
    
    def mutate(self, info, sender_id, recipient_id , content):
        
        try:
            sender = CustomUser.objects.get(pk=sender_id, user_type='consumer')
        except CustomUser.DoesNotExist:
            raise GraphQLError("sender does not exsist.")

        try:
            recipient = CustomUser.objects.get(pk=recipient_id, user_type='admin')
        except CustomUser.DoesNotExist:
            raise GraphQLError("User not found or not a consumer.")
        
        message = Message.objects.create(sender=sender, recipient=recipient, content=content)
        return CreateMessage(message=message)
        
        


class UpdateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)

    class Arguments:
        message_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, message_id, **kwargs):
       
        try:
            message = Message.objects.get(pk=message_id)
        except CustomUser.DoesNotExist:
            raise GraphQLError("Message does not exsist.")
      
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
        
        try:
            message = Message.objects.get(pk=message_id)
        except CustomUser.DoesNotExist:
            raise GraphQLError("Message does not exsist.")
        
        message.delete()
        return DeleteMessage(success=True)




# ----- Feedback -----
class CreateFeedback(graphene.Mutation):
    feedback = graphene.Field(FeedbackType)

    class Arguments:
        consumer_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, consumer_id, content):
        
        try:
            consumer = CustomUser.objects.get(pk=consumer_id, user_type='consumer' )
        except CustomUser.DoesNotExist:
            raise GraphQLError("sender does not exsist.")
        
        feedback = Feedback.objects.create(consumer=consumer, content=content)
        return CreateFeedback(feedback=feedback)
        

    
    

class UpdateFeedback(graphene.Mutation):
    feedback = graphene.Field(FeedbackType)

    class Arguments:
        feedback_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, feedback_id, **kwargs):
        
        try:
            feedback = Feedback.objects.get(pk=feedback_id)
        except Feedback.DoesNotExist:
            raise GraphQLError("Feedback does not exsist.")
        
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
        
        try:
            feedback = Feedback.objects.get(pk=feedback_id)
        except Feedback.DoesNotExist:
            raise GraphQLError("Feedback does not exsist.")
        
        feedback.delete()
        return DeleteFeedback(success=True)
    



# ----- Verification -----

class CreateVerification(graphene.Mutation):
    verification = graphene.Field(VerificationType)

    class Arguments:
        certification_id = graphene.ID(required=True)
        verified_by_id = graphene.ID(required=True)
        status = graphene.Boolean(required=True)

    def mutate(self, info, certification_id, verified_by_id, status):
        
        try:
            certification = Certification.objects.get(pk=certification_id)
        except Certification.DoesNotExist:
            raise GraphQLError("Certification not found.")

        try:
            verified_by = CustomUser.objects.get(pk=verified_by_id, user_type='consumer')
        except CustomUser.DoesNotExist:
            raise GraphQLError("User not found or not a consumer.")

        
        verification = Verification.objects.create(
            certification=certification,
            verified_by=verified_by,
            status=status,
            verification_date=timezone.now()  
        )

        return CreateVerification(verification=verification)



class UpdateVerification(graphene.Mutation):
    verification = graphene.Field(VerificationType)

    class Arguments:
        verification_id = graphene.ID(required=True)
        qr_code = graphene.String()
        verification_status = graphene.String()

    def mutate(self, info, verification_id, **kwargs):

        try:
           verification = Verification.objects.get(pk=verification_id)
        except Verification.DoesNotExist:
            raise GraphQLError("Verification ID  not found ")
        
        for key, value in kwargs.items():
            setattr(verification, key, value)
        verification.save()
        return UpdateVerification(verification=verification)



class DeleteVerification(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        verification_id = graphene.ID(required=True)

    def mutate(self, info, verification_id):
        try:
            verification = Verification.objects.get(pk=verification_id)
        except Verification.DoesNotExist:
            raise GraphQLError("Vertification not found.")
        
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
    
    