import graphene
from graphene_django.types import DjangoObjectType
from apps.verifications.models import Verification, Feedback

class VerificationType(DjangoObjectType):
    class Meta:
        model = Verification
        fields = ('id', 'certification', 'verification_date', 'status')

class FeedbackType(DjangoObjectType):
    class Meta:
        model = Feedback
        fields = ('id', 'consumer', 'content', 'timestamp')
