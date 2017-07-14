
urlpatterns = [
    url(r'^nazanin_ce419.herokuapp.com/blog/posts', views.posts_view),
    url(r'^nazanin_ce419.herokuapp.com/blog/post', views.post_item_view, views.add_post_view),
    url(r'^nazanin_ce419.herokuapp.com/blog/comments', views.comments_view),
    url(r'^nazanin_ce419.herokuapp.com/blog/comment', views.add_comment_view)
]