from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import re
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import Token, TempSignupCode
from django.views.generic.base import View
from secrets import token_hex
from django.contrib import messages


class signupView(View):

    def get(self, request):
        code = request.GET.get('code')
        if code:
            print('hello')
            temp_user = get_object_or_404(TempSignupCode, code=code)
            user = User.objects.create(
                username = temp_user.username,
                email = temp_user.email,
                password = temp_user.password
            )
            token = token_hex(24)
            Token.objects.create(user=user, token=token)
            temp_user.delete()
            return render(request, 'userCreated.html')
        else:
            return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if username and email and password:
            userCheck = User.objects.filter(username=username).exists()
            if userCheck:
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
            send_verification_email(email, tempcode)
            return render(request, 'mailSended.html')        

def send_verification_email(email, code):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = settings.SENDER_EMAIL
    message["To"] = settings.SENDER_EMAIL_PASSWORD

    text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
    html = f"""\
    <html>
    <body>
        <a href="http://localhost:8000/users/signup/?code={code}">ثبت نام</a>
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
