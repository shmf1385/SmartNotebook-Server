from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.views import View
from .models import Note


@method_decorator(csrf_exempt, name="dispatch")
class newNote(View):

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
