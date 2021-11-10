from django.db.models import fields
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from .models import Note


@method_decorator(csrf_exempt, name="dispatch")
class getNoteView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})
    
    def post(self, request):
        username = request.POST.get('username')
        token = request.POST.get('token')
        title = request.POST.get('title')
        pk = request.POST.get('pk')

        if username and token:
            user = User.objects.filter(username=username, token__token=token)
            if user:
                if title:
                    note = Note.objects.filter(
                        user = user[0],
                        title = title
                    )
                elif pk:
                    note = Note.objects.filter(
                        user = user[0],
                        pk = pk
                    )
                if note:
                    context = {
                        'title': note[0].title,
                        'content': note[0].content,
                        'pk': note[0].pk
                    }
                    return JsonResponse({"Status": "SUCCESSED", 'note': context})
                return JsonResponse({"Status": "NOTE_IS_NOTE_DEFIND"})
            return JsonResponse({"Status": "AUTHENTICATION_FAILED"})
        return JsonResponse({"Status": "ERR_ARGS"})
                

@method_decorator(csrf_exempt, name="dispatch")
class newNoteView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})

    def post(self, request):
        username = request.POST.get('username')
        token = request.POST.get('token')
        title = request.POST.get('title')
        content = request.POST.get('content')
        if username and token and content:
            user = get_object_or_404(User, token__token=token)
            if user:
                if not Note.objects.filter(title=title):
                    Note.objects.create(
                        title = title,
                        user = user,
                        content = content,
                    )
                    return JsonResponse({"Status": "FILE_CREATED"})
                return JsonResponse({"Status": "ERR_TITLE_EXISTS"})
        return JsonResponse({"Status": "ERR_LOW_ARGS"})


@method_decorator(csrf_exempt, name="dispatch")
class editNoteView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})

    def post(self, request):
        username = request.POST.get('username')
        token = request.POST.get('token')
        pk = request.POST.get('pk')
        content = request.POST.get('content')
        title = request.POST.get('title')
        
        if username and token and pk and content and title:
            user = get_object_or_404(User, token__token = token)
            if user:
                note = get_object_or_404(Note, pk = pk, user=user)
                if note:
                    note.title = title
                    note.content = content
                    note.save()
                    return JsonResponse({"Status": "NOTE_EDITED"})
        return JsonResponse({"Status": "ERR_ARGS"})
                    

@method_decorator(csrf_exempt, name="dispatch")
class deleteNoteView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})

    def post(self, request):
        username = request.POST.get('username')
        token = request.POST.get('token')
        pk = request.POST.get('pk')
        if username and token and pk:
            user = get_object_or_404(User, token__token=token)
            if user:
                note = get_object_or_404(
                    Note,
                    pk = pk,
                    user = user
                )
                if note:
                    note.delete()
                    return JsonResponse({"Status": "NOTE_DELETED"})
        return JsonResponse({"Status": "ERR_ARGS"})