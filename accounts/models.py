from django.conf import settings
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # <- 특정 사용자 모델에 종속적이지 않다.
        on_delete=models.CASCADE
    )
    phone = models.CharField(max_length=100, default='')
    birth_day = models.DateField("생일", auto_now=True)

    class Meta:
        db_table = 'accounts_profile'
        app_label = 'accounts' # <- account 앱 카테고리에서 관리되도록 한다.