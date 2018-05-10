from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import BookmarkForm, DeleteBookMarkForm
from .models import Bookmark, PersonalBookmark
import logging


logger = logging.getLogger(__name__)
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