from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        # r'^(?P<username>[\w.@+-]+)$',
        # 로그인 한 상태로 들어온다 하면
        # 해당 로그인한 user name을 받아오면 되는거다.
        r'^$',
        views.profile,
        name='profile'
    ),
]