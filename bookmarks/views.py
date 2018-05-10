from django.forms import modelformset_factory
from django.shortcuts import render
from .models import Bookmark, PersonalBookmark



# Create your views here.
def index(request):
  context = {}
  pb = PersonalBookmark.objects.values_list('id')
  context['bookmarks'] = Bookmark.objects.exclude(id__in=pb)
  if request.user.is_anonymous:
    context['personal_bookmarks'] = PersonalBookmark.objects.none()
  else:
    context['personal_bookmarks'] = PersonalBookmark.objects.filter(user = request.user)

  return render(request, 'bookmarks/index.html', context)

def bookmark_model(request):
  BookmarkFormSet = modelformset_factory(Bookmark, fields('url', 'name', 'notes'))
  if request.method == 'POST':
    formset = BookmarkFormSet(request.POST, request.FILES)
    if formset.is_valid():
      formset.save()

      return index(request)
  else:
    formset = BookmarkFormSet()
  return render(request, 'bookmarks/index.html', {'formset': formset})