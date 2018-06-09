from django.shortcuts import render, get_object_or_404

# user model로 뭔가 하려고 하면 임포트 하라.
from django.contrib.auth import get_user_model

# access control을 위한 decorator 참조용
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def profile(request) :
    # 현재 로그인중인 유저 객체를 받아옴.
    user = request.user

    storedfiles = user.storedfiles_set.order_by('-created_at', '-pk')

    ctx = {
        # template로 넘길 context 요소들
        'user1': user,
        # 정렬된 데이터를 템플릿에 변수로서 넘김
        'storedfiles': storedfiles,

    }
    return render(request, 'profile.html', ctx)

# def profile(request, username) :
#     # settings의 AUTH_USER_MODEL을 기준으로 유저모델을 가져옴.
#     User = get_user_model()
#     # User는 User model의 인스턴스이고
#     # User model은 StoredFiles와 Foreign key로 연결되어 있다.
#     user = get_object_or_404(User, username=username)

#     # view 측에서의 데이터 순서 정렬방법
#     storedfiles = user.storedfiles_set.order_by('-created_at', '-pk')

#     ctx = {
#         # template로 넘길 context 요소들
#         'user1': user,
#         # 정렬된 데이터를 템플릿에 변수로서 넘김
#         'storedfiles': storedfiles,

#     }
#     return render(request, 'profile.html', ctx)

    # 새로운 App을 시작했고 그 하위에 템플릿을 작성했다면
    # 반드시 settings.py에 INSTALLED_APPS에 해당 APP을 추가하자.
    # 그래야 template를 제대로 찾아 뿌릴 수 있다.