from django.urls import path
from .views import newNoteView, editNoteView, deleteNoteView, getNoteView

urlpatterns = [
    path('new/', newNoteView.as_view(), name="newNoteNote"),
    path('edit/', editNoteView.as_view(), name="editNoteView"),
    path('delete/', deleteNoteView.as_view(), name="deleteNoteView"),
    path('get/', getNoteView.as_view(), name="getNoteView")
]