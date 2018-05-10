from django.shortcuts import render
from .forms import BookmarkForm
from .models import Bookmark, PersonalBookmark



# Create your views here.
def index(request):
  # import pdb; pdb.set_trace()
  if request.method == 'POST':
    form = BookmarkForm(request.POST)
    if form.is_valid():
      form.save()
  context = {}
  pb = PersonalBookmark.objects.values_list('id')
  context['bookmarks'] = Bookmark.objects.exclude(id__in=pb)
  if request.user.is_anonymous:
    context['personal_bookmarks'] = PersonalBookmark.objects.none()
  else:
    context['personal_bookmarks'] = PersonalBookmark.objects.filter(user = request.user)
  
  context['form'] = BookmarkForm()

  return render(request, 'bookmarks/index.html', context)