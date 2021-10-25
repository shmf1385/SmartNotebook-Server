from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Note
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

@csrf_exempt
def newNote(request):
    if request.method == "POST":
        try:
            if request.POST['title'] and request.POST['username'] and request.POST['content']:
                pass
        except MultiValueDictKeyError:
            return JsonResponse({"Status": "ERR_LOW_ARGS"})
        if User.objects.filter(username=request.POST['username']):
            if not Note.objects.filter(title=request.POST['title']):
                Note.objects.create(
                    title = request.POST['title'],
                    user = User.objects.filter(username=request.POST['username'])[0],
                    content = request.POST['title']
                )
                return JsonResponse({"Status": "FILE_CREATED"})
            return JsonResponse({"Status": "ERR_FILENAME"})
        return JsonResponse({"Status": "ERR_USERNAME"})
    return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})