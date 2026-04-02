import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError
from decimal import Decimal
from apps.users.models import CustomUser, UserProfile
from utils.send_email import send_email
from .models import CertificationApplication, Document, ProductDetails, Certification

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
            "id", "certification_application", "custom_certification_id", "manufacturer","product",
            "first_issued", "last_issued", "modified_on", "expiry_date", "qr_code", "status", 'pdf_file'
        )

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
        try:
           certification_application = CertificationApplication.objects.get(pk=certification_application_id)
        except CertificationApplication.DoesNotExist:
            raise Exception("Certification Application not found")
        
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
            annual_production_quantity=annual_production_quantity,
            unit_selling_price=unit_selling_price,
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
        try:
           product_details = ProductDetails.objects.get(pk=product_details_id)
        except ProductDetails.DoesNotExist:
            raise Exception("Product Details not found")
        
        product_details.delete()
        return DeleteProductDetails(success=True)

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
            certification = Certification.objects.get(pk=certification_id)
        except Certification.DoesNotExist:
            raise GraphQLError("Certification does not exist.")

        certification.delete()
        return DeleteCertification(success=True)

class Mutation(graphene.ObjectType):
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
