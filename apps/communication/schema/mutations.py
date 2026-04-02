import graphene
from .types import MessageType
from apps.communication.models import Message
from apps.users.models import CustomUser

class CreateMessage(graphene.Mutation):
    message = graphene.Field(MessageType)
    class Arguments:
        sender_id = graphene.ID(required=True)
        recipient_id = graphene.ID(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_id, recipient_id, content):
        sender = CustomUser.objects.get(pk=sender_id, user_type='consumer')
        recipient = CustomUser.objects.get(pk=recipient_id, user_type='admin')
        message = Message.objects.create(sender=sender, recipient=recipient, content=content)
        return CreateMessage(message=message)

class Mutation(graphene.ObjectType):
    create_message = CreateMessage.Field()
