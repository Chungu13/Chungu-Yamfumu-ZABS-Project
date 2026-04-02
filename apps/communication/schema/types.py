import graphene
from graphene_django.types import DjangoObjectType
from apps.communication.models import Message

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content', 'timestamp')
