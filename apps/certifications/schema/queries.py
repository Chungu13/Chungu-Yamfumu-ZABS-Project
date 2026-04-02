import graphene
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from .types import CertificationApplicationType, DocumentType, ProductDetailsType, CertificationType

class Query(graphene.ObjectType):
    all_certification_applications = graphene.List(CertificationApplicationType)
    all_product_details = graphene.List(ProductDetailsType)
    all_documents = graphene.List(DocumentType)
    all_certifications = graphene.List(CertificationType)
    
    certification_application = graphene.Field(CertificationApplicationType, id=graphene.ID(required=True))
    product_detail = graphene.Field(ProductDetailsType, id=graphene.ID(required=True))
    document = graphene.Field(DocumentType, id=graphene.ID(required=True))
    certification = graphene.Field(CertificationType, id=graphene.ID(required=True))

    def resolve_all_certification_applications(self, info):
        return CertificationApplication.objects.all()
    
    def resolve_all_product_details(self, info):
        return ProductDetails.objects.all()

    def resolve_all_documents(self, info):
        return Document.objects.all()
    
    def resolve_all_certifications(self, info):
        return Certification.objects.all()

    def resolve_certification_application(self, info, id):
        return CertificationApplication.objects.get(pk=id)
    
    def resolve_product_detail(self, info, id):
        return ProductDetails.objects.get(pk=id)

    def resolve_document(self, info, id):
        return Document.objects.get(pk=id)

    def resolve_certification(self, info, id):
        try:
            return Certification.objects.get(pk=id)
        except Certification.DoesNotExist:
            return None
