from django.urls import path, include
from .views import *

urlpatterns = [
    path('create/', create_note, name='create-note'),
    path('<int:id>/', fetch_note, name='get-note'),
    path('share/', share_note, name='share-note'),
    path('update/<int:id>/', update_note, name='update-note'),
    path('version-history/<int:id>', get_changes, name='note-version')
]