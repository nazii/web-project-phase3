from django.http import HttpResponse
import json
from user.models import Token


def login_required(function=None):
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            token = request.META.get("HTTP_X_TOKEN")
            try:
                tokenObj = Token.objects.get(token=token)
            except Token.DoesNotExist:
                return HttpResponse(json.dumps({"status" : -1}),
                                    content_type="application/json")
            args = args + (tokenObj.user,)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function is None:
        return _decorator
    else:
        return _decorator(function)
