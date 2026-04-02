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
        status = graphene.String(required=True)
        quality_mark = graphene.Boolean()
        certified_local_supplier = graphene.Boolean()
        good_food_logo = graphene.Boolean()
        has_target_assessment_date = graphene.Boolean()
        target_assessment_date = graphene.Date()
        review_comment = graphene.String()
        rejection_reason = graphene.String()

    def mutate(self, info, certification_application_id, status, **kwargs):
        try:
            certification_application = CertificationApplication.objects.get(pk=certification_application_id)
            # Find related certification to get its info for the email context
            try:
                certification = Certification.objects.get(certification_application=certification_application)
                custom_id = certification.custom_certification_id
                issued_date = certification.last_issued
                pdf_link = certification.pdf_file
                qr_link = certification.qr_code
            except Certification.DoesNotExist:
                custom_id = "N/A"
                issued_date = timezone.now()
                pdf_link = ""
                qr_link = ""
                
        except CertificationApplication.DoesNotExist:
            raise GraphQLError("Certification Application not found")

        # Update fields based on kwargs
        for key, value in kwargs.items():
            setattr(certification_application, key, value)
            
        certification_application.status = status
        certification_application.save()

        # Prepare context for email
        context = {
            'user_name': certification_application.manufacturer.company_name,
            'application_id': custom_id,
            'certification_application_id': certification_application.id,
            'approval_date': issued_date,
            'pdf_link': pdf_link,
            'qr_code_link': qr_link,
            'rejection_date': timezone.now(),
            'rejection_reason': certification_application.rejection_reason,
            'submission_date': certification_application.application_date,
            'review_start_date': certification_application.application_date
        }

        # Determine email template and subject based on status
        if status == 'Approved':
            subject = "Your Certification Application is Approved"
            template_name = "approved_email.html"
        elif status == 'Rejected':
            subject = "Your Certification Application has been Rejected"
            template_name = "rejection_email.html"
        elif status == 'Submitted':
            subject = "Your Certification Application has been Submitted"
            template_name = "submitted_email.html"
        elif status == 'Reviewing':
            subject = "Your Certification Application is Under Review"
            template_name = "review_email.html"
        else:
            raise GraphQLError("Invalid status.")

        # Send the email
        try:
            send_email(subject, template_name, context, [certification_application.manufacturer.user.email])
        except Exception as e:
            # We don't want to fail the mutation if only the email fails, but let's log it
            print(f"Failed to send status email: {e}")

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

from django.utils import timezone

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

class Mutation(graphene.ObjectType):
    create_certification_application = CreateCertificationApplication.Field()
    update_certification_application = UpdateCertificationApplication.Field()
    delete_certification_application = DeleteCertificationApplication.Field()
    create_product_details = CreateProductDetails.Field()
    create_certification = CreateCertification.Field()
