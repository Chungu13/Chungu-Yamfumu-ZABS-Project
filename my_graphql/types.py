# graphql/types.py
import graphene
from graphene_django.types import DjangoObjectType
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from apps.users.models import CustomUser, UserProfile
from apps.communication.models import Message 
from apps.verifications.models import Verification, Feedback 


class CustomUserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "phone_number", "location", "user_type", "gender", "date_of_birth", "profile_picture")


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = ('id', 'manufacturer', 'company_name', 'physical_address', 'postal_address', 'contact_person',  'position', 'email', 'website')


class CertificationApplicationType(DjangoObjectType):
    class Meta:
        model = CertificationApplication
        fields = (
            "id", "manufacturer", "quality_mark", "certified_local_supplier", 
            "good_food_logo", "has_target_assessment_date", "target_assessment_date", 
            "status", "review_comment", "rejection_reason"
        )


class DocumentType(DjangoObjectType):
    class Meta:
        model = Document
        fields = ("id", "certification_application", "file", "upload_date", "file_name")


class ProductDetailsType(DjangoObjectType):
    class Meta:
        model = ProductDetails
        fields = (
            "id", "certification_application", "product_name", "description",
            "brand_or_trade_name", "standard", "supporting_documents",
            "annual_production_quantity", "unit_selling_price"
        )


class CertificationType(DjangoObjectType):
    class Meta:
        model = Certification
        fields = (
            "id", "certification_application", "certification_id", "manufacturer",
            "first_issued", "last_issued", "modified_on", "expiry_date", "qr_code", "status"
        )


       
class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content', 'timestamp')
        


class VerificationType(DjangoObjectType):
    class Meta:
        model = Verification
        fields = ('id', 'certification', 'verified_by', 'verification_date', 'status')
        
     


class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback
        fields = ('id', 'consumer', 'content', 'timestamp')           
