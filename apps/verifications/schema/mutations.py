import graphene
from .types import VerificationType, FeedbackType
from apps.verifications.models import Feedback
from apps.users.models import CustomUser

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
    create_feedback = CreateFeedback.Field()
