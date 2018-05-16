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

class DeleteNote(graphene.Mutation):
  id = graphene.String()

  class Arguments:
    id = graphene.String(required=True)
  
  def mutate(self, info, id):
    note = NoteModel.objects.get(pk=id)
    deletedNote = note.delete()

    return DeleteNote(
      "Note has been succesfully deleted"
    )

class Mutation(graphene.ObjectType):
  create_note = CreateNote.Field()
  update_note = UpdateNote.Field()
  delete_note = DeleteNote.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


