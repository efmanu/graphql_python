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

from sqlalchemy.orm import defer

from db.model import (
    User as UserModel
)



class SQLAlchemyInputObjectType(graphene.InputObjectType):
    """ 
    To Generate Graphene Mutation Inputs from SQLAlchemy Class Attributes
    https://stackoverflow.com/questions/48806710/generate-graphene-mutation-inputs-from-sqlalchemy-class-attributes

    """
    @classmethod
    def __init_subclass_with_meta__(  # pylint: disable=arguments-differ
        cls, obj_type=None, model=None, registry=None, only_fields=(), exclude_fields=(),batching=False,
        optional_fields=(), **options
    ):
        if not registry:
            registry = get_global_registry()

        connection_field_factory = default_connection_field_factory
        
        sqla_fields = yank_fields_from_attrs(
            construct_fields(obj_type, model, registry, only_fields, exclude_fields, batching, connection_field_factory),
            _as=graphene.Field,
        )

        for key, value in sqla_fields.items():
            if key in optional_fields:
                type_ = value.type if isinstance(
                    value.type, SubclassWithMeta_Meta) else value.type.of_type
                value = type_(
                    description=value.description
                )
            setattr(cls, key, value)

        super(SQLAlchemyInputObjectType, cls).__init_subclass_with_meta__(
            **options
        )


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)
        exclude_fields = ('user_id',) 


class Query(graphene.ObjectType):
    getUser = graphene.List(UserObject, username=graphene.String())

    def resolve_getUser(root, info, username=None):
        query = session.query(UserModel)
        if username is not None:
            return query.filter(UserModel.username == username).all()
        return query.all()


class CreateUserInput(SQLAlchemyInputObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)
        obj_type=UserObject
        exclude_fields = (
            'user_id',
            'id'
        )


class CreateUser(graphene.Mutation):
    class Arguments:
        user_details = graphene.List(CreateUserInput)

    users = graphene.List(UserObject)

    def mutate(self, info, user_details):

        new_users = []
        for user in user_details:
            new_user = UserModel(username=user.username, user_id=f"USER&&ID&&{str(uuid.uuid4())}", first_name=user.first_name, last_name=user.last_name)
            session.add(new_user)
            new_users.append(new_user)

        session.commit()

        return CreateUser(users=new_users)


class Mutation(graphene.ObjectType):\
    create_user = CreateUser.Field()


schema = Schema(query=Query, mutation=Mutation)