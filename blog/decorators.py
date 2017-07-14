
def login_required(request, *args, **kwargs):
    token = request.META.get["X-Token"]
    try:
        tokenObj = Token.get(token = token)
    except tokenObj.DoesNotExist:
        raise exceptions.AuthenticationFailed('No such user')

    return (tokenObj, None)



def login_required():
    def _decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            token = request.META.get["X-Token"]
            try:
                tokenObj = Token.get(token=token)
            except tokenObj.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user')
            args["userParam"] = tokenObj.user
        return _wrapped_view
    return _decorator