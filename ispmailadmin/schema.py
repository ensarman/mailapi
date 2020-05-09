import graphene
import graphql_jwt

import virtual.schema
import sys_users.schema


class Query(virtual.schema.Query,
            sys_users.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(
        virtual.schema.Mutation,
        sys_users.schema.Mutation,
        graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
