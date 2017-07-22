import datetime
import json

from django.http import HttpResponse
# Create your views here.
import logging

from blog.decorators import login_required
from blog.models import Weblog, Post, Comment

logger = logging.getLogger('django')


@login_required
def default_weblog_view(request, user_param):
    default_web = Weblog.objects.get(is_default=True, user=user_param)
    if default_web is None:
        logger.error('user has no default weblog')
    return HttpResponse(json.dumps({"id": default_web.id}),
                        content_type="application/json")


@login_required
def posts_view(request, user_param):
    s = int(request.GET.get("count"))
    e = int(request.GET.get("offset"))
    web_number = request.GET.get("web_number")
    # web = Weblog.objects.get(id=web_number, user=user_param)
    #
    # if web is None:
    #     logger.error("could not find web")

    list = Post.objects.filter(weblog__id=web_number).order_by("datetime")[s:e]
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
    time = datetime.datetime.now()
    post = Post.objects.get( id=post_id)
    cm = Comment.objects.create(text=text, time=time, post=post)
    cm.save()
    cm_json = {
        'datetime': datetime,
        'text': text
    }
    return HttpResponse(json.dumps({"status": 0, "comment": cm_json}),
                        content_type="application/json")


@login_required
def search_blog(request):
    key_words = request.POST.get("key_words").split(",")
    weblog_map = {}
    for word in key_words:
        items = Weblog.objects.filter(post_words__iexact=word)
        for web in items:
            if web not in weblog_map:
                weblog_map[web] = 0
                
            word_index = web.post_words.index(word)
            dash_index = web.post_words.index("-", word_index)
            comma_index = web.post_words.index(",", word_index)
            num = int(web.post_words[dash_index, comma_index])
            weblog_map[web] += num

    weblogs = weblog_map.items()
    if len(weblogs) <= 10:
        return HttpResponse(json.dumps({"status": 0, "weblogs": weblogs}),
                            content_type="application/json")
    for i in range(len(weblogs)):
        for j in range(i, len(weblogs), 1):
            if weblog_map[weblogs[i]] < weblog_map[weblogs[i]]:
                tmp = weblogs[i]
                weblogs[i] = weblogs[j]
                weblogs[j] = tmp

    return HttpResponse(json.dumps({"status": 0, "weblogs": weblogs[0:10]}),
                        content_type="application/json")
