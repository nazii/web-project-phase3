import datetime
import json
from django.http import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from blog.decorators import login_required
from blog.models import Weblog, Post, Comment


@login_required
def default_weblog_view(request, user_param):
    default_web = Weblog.objects.get(is_default=True, user=user_param)
    return HttpResponse(json.dumps({"id": default_web.id}),
                        content_type="application/json")


@login_required
def posts_view(request, web_number, count, offset, user_param):
    s = int(count)
    e = int(offset) + s
    web = Weblog.objects.get(name=web_number, user=user_param)
    list = Post.objects.filter(user=user_param, weblog=web).order_by("-creation_date")[s:e]
    to_return = []
    if list is not None:
        for post in list:
            to_return.append({"title": post.title, "summary": post.summary, "writer": post.writer_name})
    return HttpResponse(json.dumps({"posts": to_return}),
                        content_type="application/json")


@login_required
def post_item_view(request, user_param):
    if request.method == "GET":
        post_id = request.GET.get("id")
        web_number = request.GET.get("web_number")
        web = Weblog.objects.get(name=web_number, user=user_param)
        post = Post.objects.get(weblog=web, id=post_id)
        if post is not None:
            return HttpResponse(json.dumps({"writer": post.writer_name, "title": post.title,
                                            "text": post.text}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": -1}), content_type="application/json")
    elif request.method == "POST":
        title = request.POST.get("title")
        summary = request.POST.get("summary")
        text = request.POST.get("text")
        time = datetime.datetime.now()
        weblog_num = request.POST.get("web_number")
        web = Weblog.objects.get(name=weblog_num, user=user_param)
        post = Post.objects.create(title=title, summary=summary, text=text, time=time, web=web)
        post.save()
        post_json = {
            'title': title,
            'summary': summary,
            'text': text,
            'datetime': datetime
        }

        return HttpResponse(json.dumps({"status": 0, "post": post_json}),
                            content_type="application/json")


@login_required
def comments_view(request, user_param):
    post_id = request.GET.get("post_id")
    s = int(request.GET.get("count"))
    e = int(request.GET.get("offset"))
    list = Comment.objects.filter(user=user_param, post__id=post_id).order_by("-creation_date")[s:e]
    to_return = []
    if list is not None:
        for cm in list:
            to_return.append({"text": cm.text, "datetime": cm.datetime})
    return HttpResponse(json.dumps({"comments": to_return}),
                        content_type="application/json")


@login_required
def add_comment_view(request, user_param):
    post_id = request.POST.get("post_id")
    text = request.POST.get("text")
    web_number = request.POST("web_number")
    time = datetime.datetime.now()
    web = Weblog.objects.get(name=web_number, user=user_param)
    post = Post.objects.get(weblog=web, id=post_id)
    cm = Comment.objects.create(text=text, time=time, post=post)
    cm.save()
    cm_json = {
        'datetime': datetime,
        'text': text
    }
    return HttpResponse(json.dumps({"status": 0, "comment": cm_json}),
                        content_type="application/json")
