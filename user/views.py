import random
from string import ascii_uppercase, digits

# Create your views here.
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from blog.models import Weblog
from user.forms import LoginForm, RegisterForm
from user.models import Token


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                token_string = username.join(random.choice(ascii_uppercase + digits) for i in range(20))
                token = Token.objects.create(token=token_string, user=user)
                return HttpResponse(json.dumps({"status": 0, "token": token_string}),
                                    content_type="application/json")
            else:
                print("user not found")
                return HttpResponse(json.dumps({"status": -1}),
                                    content_type="application/json")
        return HttpResponse(json.dumps({"status": -1}),
                            content_type="application/json")
    print("form not valid")
    return HttpResponse(json.dumps({"status": -1}),
                        content_type="application/json")


def register_view(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            old_user = User.objects.filter(Q(username=username))
            if old_user is not None and len(old_user) > 0:
                print("user is not none")
                return HttpResponse(json.dumps({"status": -1}),
                                    content_type="application/json")
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            weblog = Weblog.objects.create(user=user, weblog_name="default", is_default=True)
            weblog.save()

            return HttpResponse(json.dumps({"status": 0}), content_type="application/json")

    return HttpResponse(json.dumps({"status": -1}),
                        content_type="application/json")

