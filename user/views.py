from random import choice
from string import ascii_uppercase

# Create your views here.
def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                tokenString = username.join(random.choice(ascii_uppercase + digits) for i in range(20))
                token = Token.objects.create_object(tokenString, user)
                return HttpResponse(json.dumps({"status": 0, "token" : token}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({"status": -1}),
                                    content_type="application/json")
        return HttpResponse(json.dumps({"status": -1}),
                            content_type="application/json")
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
                return HttpResponse(json.dumps({"status": -1}),
                                    content_type="application/json")
            user = User.objects.create_user(username, email, password, first_name, last_name)
            user.save()

            return HttpResponse(json.dumps({"status": 0}), content_type="application/json")
    return HttpResponse(json.dumps({"status": -1}),
                        content_type="application/json")

