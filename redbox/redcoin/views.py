from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import StoredFiles
from django.shortcuts import get_object_or_404

# Sign Up, Upload를 위한 model form
from .forms import FileUpForm, SignUpForm, LoginForm

# access control을 위해 LOGIN_URL 참조용
from django.conf import settings

# access control을 위한 decorator 참조용
from django.contrib.auth.decorators import login_required

# Sign Up을 위한 User Model 참조와 Login function
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# dynamoDB의 연결(테이블 생성, 파일정보 저장)과 관련된 기능
from .dynamo_manager import createFileList, updateFileInfo

# Create your views here.

# 참고 :
# request에는 user 속성이 있다.
# login 상태에서는 user 인스턴스가
# login이 되지 않은 상태에서는 AnonymousUser 인스턴스가 있다.

def index(request):
    if(request.method == "POST") :
        form = SignUpForm(request.POST)
        
        # form 자체에서 유효성 검사
        if(form.is_valid()) :
            # **form.cleaned_data : 유효성 및 파이썬 반환을 고려해
            # request.POST로 접근하는 것 보다 이 방법을 권장한다.
            new_user = User.objects.create_user(**form.cleaned_data)
            # user를 만들고 그 이름으로 dynamo에 file table 생성
            createFileList(request.POST['username'])
            login(request, new_user)
            return redirect('users/')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', context={'form': form})


# login을 뷰에 따로 구현하는 것에서 뷰이름을 'login'이면 안된다.
# 이미 login이 auth에 있고, 이를 우리는 사용해야 한다.
def signin(request) :
    if(request.method == "POST") :
        #form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if(user != None) :
            login(request, user)
            return redirect('/users/')
        else :
            # user를 찾지 못할 경우 or user 로그인에 실패한 경우
            return HttpResponse("Login Failed")

    else :
        form = LoginForm()
        return render(request, 'login.html', context={'form':form})




# url - view connection simple test
def hello(request) :
    return HttpResponse("Hello")

@login_required
def detail(request, pk) :
    
    storedFile = get_object_or_404(StoredFiles, pk=pk) # 여기서 pk는 models.StoredFiles의 primary_key일 것

    msg = (
        '<p>{pk}번 파일을 보여줄게여 ㅎㅎ</p>'.format(pk=storedFile.pk),
        '<p>주소는 {url}</p>'.format(url=storedFile.content.url),
        '<p>user key : {user}</p>'.format(user=storedFile.user),
        '<p>Onwer : {owner}</p>'.format(owner=storedFile.owner),
        '<p><img src={url} /></p>'.format(url=storedFile.thumnail.url),

    )
    return HttpResponse('\n'.join(msg))

# 아래의 user.is_authencated를 한문장으로 간소화시켜줌.
# 이럴꺼면 밑에꺼 왜했나.... 자괴감들어...
# login 후 이동할 주소 => setting.LOGIN_URL로 자동 지정됨.
@login_required
def create(request) :

    # login 한 유저인지에 대한 여부
    # request.user의 is_authenticated() 메서드 사용 => X
    # user.is_authenticated => O
    # 메서드가 아니라 property로 바뀜.
    # bool값으로 반환함 => X => 그냥 자체로 property임.
    # if( not request.user.is_authenticated ) :
    #     return redirect(settings.LOGIN_URL)

    if(request.method == "GET") :
        form = FileUpForm()

    # 게시물 내용과 파일을 제출받는(??) 부분
    elif(request.method == "POST") :

        #  request.POST : form에서 다룰 데이터.
        #                 dict or similar to dict 여야 한다.
        #                 파일을 제외한 HTML에서 POST 방식으로 전송한
        #                 모든 form 데이터가 여기에 있다.
        # request.FILES : 파일은 여기에 있다.
        #
        # 그래서 두개로 나누어서 인자로 전달한 것이다.
        form = FileUpForm(request.POST, request.FILES)

        if(form.is_valid()) : # form 검증
            # form = FileUpForm이고
            # FileUpForm은 model과 연결되어 있으므로
            # 데이터를 저장하게 되는 것
            #
            # form이 ModelForm을 상속한 경우 save() 메서드를 가지고 있음.
            # 이 save() 메서드는 model의 save()와 같은 역할임.
            # data가 저장된 것을 반영한 model의 인스턴스를 반환

            # obj = form.save()
            # 즉, obj는 form에 연결되어 있는 model로 생성한 인스턴스이다.
            # commit=False 속성은 DB에 바로는 반영하지 말아달라고 하는 것.
            obj = form.save(commit=False)
            # 이유는 user에 대한 정보를 넘기기 위해서
            # 여러가지 보안상의 문제가 있지만, 여기서는 편하게
            # 잠시 commit=False로 하고 아래와 같인 직접 할당.
            obj.user = request.user
            # 그리고 최종 save()를 통해 유저정보까지 DB에 반영.            
            obj.save()

            # 해당 파일 로컬 업로드 후에 dynamo에 해당 파일에 대한 정보 업데이트
            updateFileInfo(request.user.username,obj.content.url,obj.content.url)

            # redirect는 지정한 URL로 이동(?)시킨다.
            # 만약 인자가 model의 인스턴스라면
            # 그 객체의 get_absolute_url() 실행
            return redirect(obj)

    ctx = {
        # key : tempalte파일 안에서 쓰여지는 변수의 이름
        'form1': form,
    }

    return render(request, 'edit.html', ctx)
