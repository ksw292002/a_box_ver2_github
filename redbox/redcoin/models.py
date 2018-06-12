from django.db import models

# views.py에서 redirect를 위해
# from django.core.urlresolvers import reverse_lazy
# django 1.10 ~ : django.core.urlresolvers => django.urls
from django.urls import reverse_lazy

# 관계모델 필드의 AUTH_USER_MODEL 참조용
from django.conf import settings

# Create your models here.


class StoredFiles(models.Model) :
    file_number = models.AutoField(primary_key=True) # 자동으로 증가하는 file_number
    owner = models.CharField(max_length=50) # 이 파일을 소유하고 있는 user의 id
    # content = models.FileField(upload_to='%Y/%m/%d/content')
    # thumnail = models.ImageField(upload_to='%Y/%m/%d/thumnail')
    content = models.FileField(upload_to='content')
    thumnail = models.ImageField(upload_to='thumnail')
    description = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # 파일 추가되면 그 시간 기록

    # 장고 관계모델 필드
    # django 2.x부터 on_delete argument 필수
    # on_delete=models.CASCADE 추가하자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # StoredFiles 쪽에서 user로 일방적인 ForeignKey를 맺었다.
    # 우리는 알 수 있지만, 파이썬은 user model이 ForeignKey를 맺었는지 어떤지 알 길이 없다.
    # 그래서 한쪽에서 ForeignKey를 맺게 되면(N쪽이다),
    # 맺어진 쪽에서는 N쪽의 모델이름을 소문자로 만들고 _set을 붙인 이름의 속성을 만든다.(1쪽이다)
    # 그래서 user model은 'storedfiles_set'이라는 속성을 가지게 되는 것이다.
    # 이것이 '연관객체 참조속성'이다.
    # 그리고 이 연관객체 참조속성은 장고의 QuerySet 객체이다.

    # user.storedfiles_set.all()과
    # StoredFiles.objects.filter(user=user).all()와
    # 동일한 역할을 하고 있고
    # _set이 QuerySet이라는 것을 인지하고 있으면 된다.


    # class Meta :
    #     # 모델 측에서의 데이터 순서 정렬방법
    #     # 모델의 기본 정렬을 최근 등록된 순서로
    #     # 동일한 일시라면 큰 pk순서로
    #     ordering = ('-created_at', '-pk', )


    def delete(self, *args, **kwargs) :
        self.content.delete()
        self.thumnail.delete()
        super(StoredFiles, self).delete(*args, **kwargs)

    # views.py에서 model instance 받을 시
    # redirect를 위해 구현
    # get_absoulte_url()은 django의 관례의 이름
    # custom 가능
    def get_absolute_url(self) :
        url = reverse_lazy('detail', kwargs={'pk': self.pk})
        
        # url 만들었으면 꼭 return해서 pk를 넘기자.
        return url
