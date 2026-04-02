import graphene
from apps.verifications.models import Verification, Feedback
from .types import VerificationType, FeedbackType

class Query(graphene.ObjectType):
    all_verifications = graphene.List(VerificationType)
    all_feedbacks = graphene.List(FeedbackType)
    verification = graphene.Field(VerificationType, id=graphene.ID(required=True))
    feedback = graphene.Field(FeedbackType, id=graphene.ID(required=True))

    def resolve_all_verifications(self, info):
        return Verification.objects.all()

    def resolve_all_feedbacks(self, info):
        return Feedback.objects.all()

    def resolve_verification(self, info, id):
        return Verification.objects.get(pk=id)

    def resolve_feedback(self, info, id):
        return Feedback.objects.get(pk=id)
