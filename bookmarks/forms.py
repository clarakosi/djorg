from django import forms
from .models import Bookmark, PersonalBookmark

class BookmarkForm(forms.ModelForm):
  """Form to create or edit bookmarks."""
  class Meta:
    model = Bookmark
    fields = ('url', 'name', 'notes')
