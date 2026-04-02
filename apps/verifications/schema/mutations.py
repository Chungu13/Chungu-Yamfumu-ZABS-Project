import graphene
from .types import VerificationType, FeedbackType
from apps.verifications.models import Verification, Feedback
from apps.certifications.models import Certification
from apps.users.models import CustomUser

class CreateVerification(graphene.Mutation):
    verification = graphene.Field(VerificationType)

    class Arguments:
        certification_id = graphene.ID(required=True)
        status = graphene.Boolean()

    def mutate(self, info, certification_id, status=True):
        try:
            certification = Certification.objects.get(pk=certification_id)
        except Certification.DoesNotExist:
            raise Exception("Certification not found")
        
        verification = Verification.objects.create(
            certification=certification,
            status=status
        )
        return CreateVerification(verification=verification)

class CreateFeedback(graphene.Mutation):
    feedback = graphene.Field(FeedbackType)
    class Arguments:
        consumer_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, consumer_id, content):
        consumer = CustomUser.objects.get(pk=consumer_id, user_type='consumer')
        feedback = Feedback.objects.create(consumer=consumer, content=content)
        return CreateFeedback(feedback=feedback)

class Mutation(graphene.ObjectType):
    create_verification = CreateVerification.Field()
    create_feedback = CreateFeedback.Field()
