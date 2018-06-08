from django.shortcuts import render, get_object_or_404

# user model로 뭔가 하려고 하면 임포트 하라.
from django.contrib.auth import get_user_model

# Create your views here.

def profile(request, username) :
    # settings의 AUTH_USER_MODEL을 기준으로 유저모델을 가져옴.
    User = get_user_model()
    user = get_object_or_404(User, username=username)

    ctx = {
        # template로 넘길 context 요소들
        'user1': user,

    }
    return render(request, 'profile.html', ctx)

    # 새로운 App을 시작했고 그 하위에 템플릿을 작성했다면
    # 반드시 settings.py에 INSTALLED_APPS에 해당 APP을 추가하자.
    # 그래야 template를 제대로 찾아 뿌릴 수 있다.