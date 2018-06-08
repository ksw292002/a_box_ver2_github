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
    content = models.FileField(upload_to='%Y/%m/%d/content')
    thumnail = models.ImageField(upload_to='%Y/%m/%d/thumnail')
    description = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # 파일 추가되면 그 시간 기록

    # 장고 관계모델 필드
    # django 2.x부터 on_delete argument 필수
    # on_delete=models.CASCADE 추가하자
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


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
