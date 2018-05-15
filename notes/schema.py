from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from graphene import InputObjectType
from .models import Note as NoteModel

class Note(DjangoObjectType):
  class Meta:
    model = NoteModel
    interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
  notes = graphene.List(Note)

  def resolve_notes(self, info):
    user = info.context.user
    if settings.DEBUG:
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
    note = NoteModel(title=title, content=content)
    note.save()

    return CreateNote(
      id = note.id,
      title = note.title,
      content = note.content,
    )

class Mutation(graphene.ObjectType):
  create_note = CreateNote.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


