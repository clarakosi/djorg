from django.db.utils import IntegrityError
from django.test import TestCase
from .models import Bookmark

# Create your tests here.
class  BookmarkTestCase(TestCase):
  def setUp(self):
    Bookmark.objects.create(name='Example bookmark', url='http://www.example.com')
    Bookmark.objects.create(name='Google', url='http://Google.com', notes='Search engine')
  
  def test_retrieving_all_bookmarks(self):
    """Test that there are the expected number of bookmarks"""
    bookmarks = Bookmark.objects.all()
    self.assertEqual(len(bookmarks), 2)

  def test_retrieving_bookmarks_by_name(self):
    bookmark = Bookmark.objects.get(name='Google')
    self.assertEqual(bookmark.name, 'Google')
    self.assertEqual(bookmark.notes, 'Search engine')
    self.assertEqual(bookmark.url, 'http://Google.com')

  def test_retrieving_bookmarks_by_url(self):
    bookmark = Bookmark.objects.get(url='http://www.example.com')
    self.assertEqual(bookmark.name, 'Example bookmark')
    self.assertEqual(bookmark.notes, '')
    self.assertEqual(bookmark.url, 'http://www.example.com')

  def test_dupe_urls(self):
    with self.assertRaises(IntegrityError) as context:
      Bookmark.objects.create(name='Another one', url='http://Google.com')
    
    self.assertTrue('UNIQUE constraint failed: bookmarks_bookmarks.url', str(context.exception))

