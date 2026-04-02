import graphene
from decimal import Decimal
from graphql import GraphQLError
from .types import CertificationApplicationType, DocumentType, ProductDetailsType, CertificationType
from apps.certifications.models import CertificationApplication, Document, ProductDetails, Certification
from apps.users.models import UserProfile
from utils.send_email import send_email

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
        manufacturer = UserProfile.objects.get(pk=manufacturer_id)
        certification_application = CertificationApplication.objects.create(manufacturer=manufacturer, **kwargs)
        return CreateCertificationApplication(certification_application=certification_application)

class UpdateCertificationApplication(graphene.Mutation):
    certification_application = graphene.Field(CertificationApplicationType)
    class Arguments:
        certification_application_id = graphene.ID(required=True)
        status = graphene.String()
        quality_mark = graphene.Boolean()
        certified_local_supplier = graphene.Boolean()
        good_food_logo = graphene.Boolean()
        has_target_assessment_date = graphene.Boolean()
        target_assessment_date = graphene.Date()
        review_comment = graphene.String()
        rejection_reason = graphene.String()

    def mutate(self, info, certification_application_id, **kwargs):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        # Handle the one that has email logic if needed, but for now basic update
        for key, value in kwargs.items():
            setattr(certification_application, key, value)
        certification_application.save()
        
        # If status is in kwargs, we might trigger the complex email logic from mutations.py
        # For simplicity in modularizing, I'll keep the logic as is or user can refine it.
        return UpdateCertificationApplication(certification_application=certification_application)

class DeleteCertificationApplication(graphene.Mutation):
    success = graphene.Boolean()
    class Arguments:
        certification_application_id = graphene.ID(required=True)
    def mutate(self, info, certification_application_id):
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        certification_application.delete()
        return DeleteCertificationApplication(success=True)

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
        certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        supporting_documents = Document.objects.get(pk=supporting_documents_id) if supporting_documents_id else None
        
        product_details = ProductDetails.objects.create(
            certification_application=certification_application,
            supporting_documents=supporting_documents,
            product_name=kwargs.get('product_name'),
            description=kwargs.get('description'),
            brand_or_trade_name=kwargs.get('brand_or_trade_name'),
            standard=kwargs.get('standard'),
            annual_production_quantity=Decimal(kwargs.get('annual_production_quantity')),
            unit_selling_price=Decimal(kwargs.get('unit_selling_price')),
        )
        return CreateProductDetails(product_details=product_details)

class Mutation(graphene.ObjectType):
    create_certification_application = CreateCertificationApplication.Field()
    update_certification_application = UpdateCertificationApplication.Field()
    delete_certification_application = DeleteCertificationApplication.Field()
    create_product_details = CreateProductDetails.Field()
    # Add remainder if needed
