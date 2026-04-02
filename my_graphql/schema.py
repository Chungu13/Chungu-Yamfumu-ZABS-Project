import graphene
from apps.users.schema import Query as UserQuery, Mutation as UserMutation
from apps.certifications.schema import Query as CertQuery, Mutation as CertMutation
from apps.communication.schema import Query as CommQuery, Mutation as CommMutation
from apps.verifications.schema import Query as VerifQuery, Mutation as VerifMutation

class Query(UserQuery, CertQuery, CommQuery, VerifQuery, graphene.ObjectType):
    pass

class Mutation(UserMutation, CertMutation, CommMutation, VerifMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
