from django.conf import settings
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene
import graphql_jwt
from graphene import InputObjectType
from django.contrib.auth.models import Permission
from uuid import uuid4
from django.db import models
from .models import Note as NoteModel


class Note(DjangoObjectType):
  class Meta:
    model = NoteModel
    interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
  notes = graphene.List(Note)

  def resolve_notes(self, info):
    user = info.context.user
    if user.is_superuser:
      return NoteModel.objects.all()
    elif user.is_anonymous:
      return NoteModel.objects.none()
    else:
      return NoteModel.objects.filter(user=user)

class CreateNote(graphene.Mutation):
  id = graphene.String()
  title = graphene.String()
  content = graphene.String()

  class Arguments:
    title = graphene.String()
    content = graphene.String()

  def mutate(self, info, title, content):
    user = info.context.user
    note = NoteModel(title=title, content=content, user=user)
    note.save()

    return CreateNote(
      id = note.id,
      title = note.title,
      content = note.content,
    )

class UpdateNote(graphene.Mutation):
  id = graphene.String()
  title = graphene.String()
  content = graphene.String()

  class Arguments:
    id = graphene.String(required=True)
    title = graphene.String(required=False)
    content = graphene.String(required=False)
  
  def mutate(self, info, id, title, content):
    user = info.context.user
    note = NoteModel.objects.get(pk=id)
    if user == note.user:
      if len(title) > 0:
        note.title = title
        note.save()
      if len(content) > 0:
        note.content = content
        note.save()

      return UpdateNote(
        id = note.id,
        title = note.title,
        content = note.content,
      )
    else:
      return UpdateNote("You do not have permission to change this note.")

class DeleteNote(graphene.Mutation):
  id = graphene.String()

  class Arguments:
    id = graphene.String(required=True)
  
  def mutate(self, info, id):
    user = info.context.user
    note = NoteModel.objects.get(pk=id)
    if user == note.user:
      deletedNote = note.delete()

      return DeleteNote(
        "Note has been succesfully deleted"
      )
    else:
      return DeleteNote("You do not have permission to delete this note.")

class UserType(DjangoObjectType):
  class Meta:
    model = get_user_model()

class CreateUser(graphene.Mutation):
  user = graphene.Field(UserType)

  class Arguments:
    username = graphene.String(required=True)
    password = graphene.String(required=True)

  
  def mutate(self, info, username, password):
    user = get_user_model()(
      username=username
    )
    user.set_password(password)
    user.save()

    permission = Permission.objects.get(name='Can add note')
    user.user_permissions.add(permission)
    user.user_permissions.add(Permission.objects.get(name='Can change note'))
    user.user_permissions.add(Permission.objects.get(name='Can delete note'))

    user.save()   

    return CreateUser(user)

      
class Mutation(graphene.ObjectType):
  create_note = CreateNote.Field()
  update_note = UpdateNote.Field()
  delete_note = DeleteNote.Field()
  create_user = CreateUser.Field()
  token_auth = graphql_jwt.ObtainJSONWebToken.Field()
  verify_token = graphql_jwt.Verify.Field()
  refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


