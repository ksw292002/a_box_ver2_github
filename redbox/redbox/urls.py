"""redbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views  # 이 줄 추가. auth
from redcoin.views import hello, detail

# 밑에 두개 static 파일 설정
from django.conf import settings
from django.conf.urls.static import static

# create라는, model form 기능을 사용하기 위해 views에서 import
# 그리고 Sign Up을 사용하기 위해
from redcoin.views import create, index

urlpatterns = [
    url(r'^hello/$', hello), # url HttpResponse simple testing
    url(r'^storedfiles/(?P<pk>[0-9]+)/$', detail, name='detail'),
    url(r'^storedfiles/upload/$', create, name='create'),
    url(r'^redcoin/', include('redcoin.urls')),
    url(r'^users/', include('profiles.urls')),
    path('admin/', admin.site.urls),
    url(
        r'^accounts/login/',
        # django.contrib.auth.views를 auth_views로 위에 설정했고,
        # 이것의 login 뷰함수를 작동시킴
        auth_views.login,
        name='login',
        
        # 추가로 전할달 인자
        kwargs={
            # template 중 선택
            'template_name': 'login.html'
        }
    ),
    url(
        r'^accounts/logout/',
        # django.contrib.auth.views를 auth_views로 위에 설정했고,
        # 이것의 logout 뷰함수를 작동시킴
        auth_views.logout,
        name='logout',

        # 추가로 전할달 인자
        kwargs={
            # next_page : 로그아웃 후 이동할 url
            # 이 항목이 없으면 기본 django logout page로 이동
            # LOGIN_URL은 기본적으로는 /accounts/login/ 으로 지정되어있음
            'next_page': settings.LOGIN_URL,
        }
    ),
    
    # index를 통한 sign up function
    url(r'^$', index, name = 'index'),
    
]

# setting.LOGIN_REDIRECT_URL : 로그인 후 이동할 페이지를
# 별도 지정하지 않으면 이 사항에 따라서 이동하게 된다.
# 로그인을 시도하면 url이 /accounts/profile/ 이라고 되어 있는데
# 이것이 기본 값이다. 설정하면 바꿀 수 있음.


# static url 추가 
urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )