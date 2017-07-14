from django.shortcuts import render

# Create your views here.

@login_required
def default_weblog_view(userParam):
    default_web = Weblog.objects.get(is_default=True, user=userParam)
    return HttpResponse(json.dumps({"id": default_web.id}),
                        content_type="application/json")

@login_required
def posts_view(request, web_number, count, offset, userParam):
    s = int(count)
    e = int(offset) + s
    web = Weblog.objects.get(name=web_number, user=userParam)
    list = Post.objects.filter(user=userParam, weblog=web).order_by("-creation_date")[s:e]
    to_return = []
    if list is not None:
        for post in list:
            to_return.append({"title" : post.title, "summary" : post.summary, "writer" : post.writer_name})
    return HttpResponse(json.dumps({"posts": to_return}),
                        content_type="application/json")


@login_required
def post_item_view(request, userParam):
    post_id = request.GET.get("id")
    web_number = request.GET.get("web_number")
    web = Weblog.objects.get(name=web_number, user=userParam)
    post = Post.objects.get(weblog=web, id=post_id)
    if post not None :
        return HttpResponse(json.dumps({"writer": post.writer_name, "title" : post.title,
                                    "text" : post.text}),
                        content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status" : -1}),content_type="application/json")

@login_required
def comments_view(request, userParam):
    post_id = request.GET.get("post_id")
    s = int(request.GET.get("count"))
    e = int(request.GET.get("offset"))
    list = Commet.objects.filter(user=userParam, post__id=post_id).order_by("-creation_date")[s:e]
    to_return = []
    if list is not None:
        for cm in list:
            to_return.append({"text": cm.text, "datetime" : cm.datetime})
    return HttpResponse(json.dumps({"comments": to_return}),
                        content_type="application/json")

@login_required
def add_comment_view(request, userParam):
    post_id = request.POST.get("post_id")
    text = request.POST.get("text")
    datetime = datetime.datetime.now()
    web = Weblog.objects.get(name=web_number, user=userParam)
    post = Post.objects.get(weblog=web, id=post_id)
    cm = Comment.objects.create_object(text, datetime, post)
    cm.save()
    cmJson = {
        'datetime' : datetime,
        'text' : text
    }
    return HttpResponse(json.dumps({"status": 0, "comment" : cmJson}),
                        content_type="application/json")

@login_required
def add_post_view(request, userParam):
    title = request.POST.get("title")
    summary = request.POST.get("summary")
    text = request.POST.get("text")
    datetime = datetime.datetime.now()
    weblog_num = request.POST.get("web_number")
    web = Weblog.objects.get(name=weblog_num, user=userParam)
    post = Post.objects.create_object(title, summary, text, datetime, web)
    post.save()
    postJson = {
        'title' : title,
        'summary' : summary,
        'text' : text,
        'datetime' : datetime
    }

    return HttpResponse(json.dumps({"status": 0, "post": postJson}),
                        content_type="application/json")
