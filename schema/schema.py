import graphene
from graphene import relay, ObjectType, String, Field, Schema, Mutation
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from db.model import session
import uuid

from graphene.types.utils import yank_fields_from_attrs
from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
from graphene_sqlalchemy.registry import get_global_registry
from graphene_sqlalchemy.types import construct_fields
from graphene_sqlalchemy.fields import default_connection_field_factory

from db.model import (
    User as UserModel
)




class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

class Query(graphene.ObjectType):
    getUser = graphene.List(UserObject, username=graphene.String())

    def resolve_getUser(root, info, username=None):
        query = session.query(UserModel)
        if username is not None:
            return query.filter(UserModel.username == username)
        return query.all()



schema = Schema(query=Query)