import graphene
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from apps.users.models import CustomUser, UserProfile
from apps.communication.models import Message
from apps.verifications.models import Verification, Feedback
from .types import ( CustomUserType, CertificationApplicationType, DocumentType, ProductDetailsType,
                    CertificationType, UserProfileType, MessageType, VerificationType,FeedbackType)



class Query(graphene.ObjectType):
    
    # For Querying all fields
    all_custom_users = graphene.List(CustomUserType)
    all_user_profiles = graphene.List(UserProfileType)
    all_certification_applications = graphene.List(CertificationApplicationType)
    all_product_details = graphene.List(ProductDetailsType)
    all_documents = graphene.List(DocumentType)
    all_certifications = graphene.List(CertificationType)
    all_messages = graphene.List(MessageType)
    all_verifications = graphene.List(VerificationType)
    all_feedbacks = graphene.List(FeedbackType)
    
    # For quering individual fields 
    custom_user = graphene.Field(CustomUserType, id=graphene.ID(required=True))
    user_profile = graphene.Field(UserProfileType, id=graphene.ID(required=True))
    certification_application = graphene.Field(CertificationApplicationType, id=graphene.ID(required=True))
    product_detail = graphene.Field(ProductDetailsType, id=graphene.ID(required=True))
    document = graphene.Field(DocumentType, id=graphene.ID(required=True))
    certification = graphene.Field(CertificationType, id=graphene.ID(required=True)) 
    message = graphene.Field(MessageType, id=graphene.ID(required=True))
    verification = graphene.Field(VerificationType, id=graphene.ID(required=True))
    feedback = graphene.Field(FeedbackType, id=graphene.ID(required=True))
    
    
    
    
# Resolvers for all item queries
# These functions know what exaclty  and where the data is 


    def resolve_all_custom_users(self, info):
        return CustomUser.objects.all()
    
    def resolve_all_user_profiles(self, info):
        return UserProfile.objects.all()
    
    def resolve_all_certification_applications(self, info):
        return CertificationApplication.objects.all()
    
    def resolve_all_product_details(self, info):
        return ProductDetails.objects.all()

    def resolve_all_documents(self, info):
        return Document.objects.all()
    
    def resolve_all_certifications(self, info):
        return Certification.objects.all()
    
    def resolve_all_messages(self, info):
        return Message.objects.all()
    
    def resolve_all_verifications(self, info):
        return Verification.objects.all()
    
    def resolve_all_feedbacks(self, info):
        return Feedback.objects.all()
    
    


# Resolvers for single item queries
    def resolve_custom_user(self, info, id):
        return CustomUser.objects.get(pk=id)
    
    def resolve_user_profile(self, info, id):
        return UserProfile.objects.get(pk=id)

    def resolve_certification_application(self, info, id):
        return CertificationApplication.objects.get(pk=id)
    
    def resolve_product_detail(self, info, id):
        return ProductDetails.objects.get(pk=id)

    def resolve_document(self, info, id):
        return Document.objects.get(pk=id)

    # def resolve_certification(self, info, id):
    #     return Certification.objects.get(pk=id)
    
    
    
    def resolve_certification(root, info, id):
        try:
            return Certification.objects.get(id=id)
        except Certification.DoesNotExist:
            return None
    
    
    def resolve_message(self, info, id):
        return Message.objects.get(pk=id)
    
    def resolve_verification(self, info, id):
        return Verification.objects.get(pk=id)
    
    def resolve_feedback(self, info, id):
        return Feedback.objects.get(pk=id)
    
    
    


   
    
    