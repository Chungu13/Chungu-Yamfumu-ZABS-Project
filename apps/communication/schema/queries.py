import graphene
from apps.communication.models import Message
from .types import MessageType

class Query(graphene.ObjectType):
    all_messages = graphene.List(MessageType)
    message = graphene.Field(MessageType, id=graphene.ID(required=True))

    def resolve_all_messages(self, info):
        return Message.objects.all()

    def resolve_message(self, info, id):
        return Message.objects.get(pk=id)
