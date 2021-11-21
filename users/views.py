from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from secrets import token_hex
import re
import smtplib
import ssl
from .models import Token, TempSignupCode, UserDevice
from notes.models import Note


@method_decorator(csrf_exempt, name="dispatch")
class loginView(View):

    def get(self, request):
        return JsonResponse({"Stauts": "ERR_REQUEST_TYPE_IS_GET"})
    
    def post(self, request):
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        deviceName = request.POST.get("deviceName")
        ip = request.POST.get("ip")
        if email and password and deviceName and ip:
            userCheck = User.objects.filter(
                email = email,
                password = password
            )
        elif username and password and deviceName and ip:
            userCheck = User.objects.filter(
                username = username,
                password = password
            )
        else:
            return JsonResponse({"Status": "ERR_ARGS"})
        if userCheck:
            token = Token.objects.get(user=userCheck[0])
            deviceNameCheck = UserDevice.objects.filter(user = userCheck[0], device_name = deviceName)
            if not deviceNameCheck:
                now = timezone.now()
                UserDevice.objects.create(
                    user=userCheck[0],
                    device_name = deviceName,
                    ip = ip,
                    last_login = now,
                    first_login = now,
                    )
            else:
                now = timezone.now()
                deviceNameCheck[0].last_login = now
                deviceNameCheck[0].save()
            return JsonResponse({"Status": "SUCCESSED", "TOKEN": token.token})
        return JsonResponse({"Status": "AUTHENTICATION_FAILED"})


class signupView(View):

    def get(self, request):
        code = request.GET.get('code')
        if code:
            temp_user = get_object_or_404(TempSignupCode, code=code)
            user = User.objects.create(
                username = temp_user.username,
                email = temp_user.email,
                password = temp_user.password
            )

            loop = True
            while loop:
                token = token_hex(24)
                if not Token.objects.filter(token=token):
                    loop = False
                continue
            Token.objects.create(user=user, token=token)
            temp_user.delete()
            return render(request, 'userCreated.html')
        else:
            return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username and email and password:
            if validateUsername(username):
                if validateEmail(email):
                    usernameCheck = User.objects.filter(username=username).exists()
                    if usernameCheck:
                        messages.add_message(request, messages.WARNING, 'نام کاربری وارد شده قبلا توسط فردی دیگر استفاده شده است لطفا دوباره تلاش نکنید')
                        return render(request, 'signup.html', {'alertType': "danger"})
                    emailCheck = User.objects.filter(email=email).exists()
                    if emailCheck:
                        messages.add_message(request, messages.WARNING, 'ایمیل وارد شده قبلا توسط فردی دیگر استفاده شده است لطفا دوباره تلاش نکنید')
                        return render(request, 'signup.html', {'alertType': "danger"})
                    if len(password) < 8:
                        messages.add_message(request, messages.WARNING, 'طول رمز عبور حداقل ۸ کاراکتر است')
                        return render(request, 'signup.html', {'alertType': "danger"})
                    tempcode = token_hex(24)
                    TempSignupCode.objects.create(
                        code = tempcode,
                        username = username,
                        email = email,
                        password = password
                    )
                    send_verification_email(email, tempcode, request.build_absolute_uri())
                    return render(request, 'mailSended.html')
                messages.add_message(request, messages.WARNING, 'ایمیل وارد شده معتبر نمی باشد')
                return render(request, 'signup.html', {'alertType': "danger"})
            messages.add_message(request, messages.WARNING, 'نام کاربری نباید دارای فاصله باشد')
            return render(request, 'signup.html', {'alertType': "danger"})
        return JsonResponse({"Status": "ERR_ARGS"})

@method_decorator(csrf_exempt, name="dispatch")
class deleteUserView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})

    def post(self, request):
        username = request.POST.get("username")
        token = request.POST.get("token")
        if username and token:
            userCheck = User.objects.filter(username=username, token__token=token)
            if userCheck:
                userCheck[0].delete()
                userNotes = Note.objects.filter(user=userCheck[0])
                if userNotes:
                    for note in userNotes:
                        note.delete()
                userDeviceses = UserDevice.objects.filter(user=userCheck[0])
                if userDeviceses:
                    for device in userDeviceses:
                        device.delete()
                return JsonResponse({"Status": "SUCCESSED"})
            return JsonResponse({"Status": "AUTHENTICATION_FAILED"})
        return JsonResponse({"Status": "ERR_ARGS"})

@method_decorator(csrf_exempt, name="dispatch")
class checkTokenView(View):

    def get(self, request):
        return JsonResponse({"Status": "ERR_REQUEST_TYPE_IS_GET"})
    
    def post(self, request):
        username = request.POST.get('username')
        token = request.POST.get('token')
        if username and token:
            user = User.objects.filter(username=username, token__token=token)
            if user:
                return JsonResponse({"Status": "USERANME_AND_TOKEN_IS_CORRECT"})
            return JsonResponse({"Status": "USERNAME_OR_TOKEN_IS_INCORRCET"})
        return JsonResponse({"Status": "ERR_ARGS"})

def send_verification_email(email, code, absolute_uri):
    message = MIMEMultipart("alternative")
    message["Subject"] = "ثبت نام در دفترچه یادداشت هوشمند"
    message["From"] = settings.SENDER_EMAIL
    message["To"] = settings.SENDER_EMAIL_PASSWORD

    text = "لینک تایید ثبت نام شما برای دفترچه یادداشت هوشمند"
    html = f"""\
    <html>
    <body>
        <a href="{absolute_uri}?code={code}">ثبت نام</a>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(settings.SENDER_EMAIL, settings.SENDER_EMAIL_PASSWORD)
        server.sendmail(
            settings.SENDER_EMAIL, email, message.as_string()
        )

def validateEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False

def validateUsername(username):
    if " " not in username:
        return True
    return False
