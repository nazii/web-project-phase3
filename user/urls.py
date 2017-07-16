from django.conf.urls import url

from user import views


urlpatterns = [
    url(r'^nazanin_ce419.herokuapp.com/user/register', views.register_view),
    url(r'^nazanin_ce419.herokuapp.com/user/login', views.login_view)

]