from django.conf.urls import url

from user import views


urlpatterns = [
    url(r'^register$', views.register_view),
    url(r'^login$', views.login_view)

]