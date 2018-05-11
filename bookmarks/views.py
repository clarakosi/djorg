from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import BookmarkForm
from .models import Bookmark, PersonalBookmark


# Create your views here.
def index(request):
  # import pdb; pdb.set_trace()
  if request.method == 'POST':
    form = BookmarkForm(request.POST)
    if form.is_valid():
      form.save()
    else:
      messages.info(request, "This url bookmark already exists.")
  
  context = {}
  pb = PersonalBookmark.objects.values_list('id')
  context['bookmarks'] = Bookmark.objects.exclude(id__in=pb)
  if request.user.is_anonymous:
    context['personal_bookmarks'] = PersonalBookmark.objects.none()
  else:
    context['personal_bookmarks'] = PersonalBookmark.objects.filter(user = request.user)
  
  context['form'] = BookmarkForm()

  return render(request, 'bookmarks/index.html', context)

def delete_Bookmark(request, bookmark_id):
  bookmark_to_delete = get_object_or_404(Bookmark, id=bookmark_id)
  
  if bookmark_to_delete:
    bookmark_to_delete.delete()
  
  return HttpResponseRedirect('/bookmarks')

def update_BookMark(request, bookmark_id):
  bookmark_to_update = get_object_or_404(Bookmark, id=bookmark_id)

  if request.method == 'POST':
    form = BookmarkForm(request.POST)
    if form.is_valid():
      form.save()
  context = {}
  context['form'] == BookmarkForm(bookmark_to_update)
  return render(request, 'bookmarks/index.html', context)

def redirect_Nav(request):
  return HttpResponseRedirect('/')