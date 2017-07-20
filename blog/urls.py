from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^blog_id$', views.default_weblog_view),
    url(r'^posts$', views.posts_view),
    url(r'^post$', views.post_item_view),
    url(r'^comments$', views.comments_view),
    url(r'^comment$', views.add_comment_view)
]