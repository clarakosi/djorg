from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('delete/<bookmark_id>', views.delete_Bookmark, name='delete'),
  path('update/<bookmark_id>', views.update_BookMark, name='update')
]