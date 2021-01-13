from django.db import models
#from django.contrib.auth.models import User
from django.conf import settings
import datetime

# Create your models here.
class ReceiptList(models.Model):
    receipt_date = models.DateField("접수날짜", default=datetime.datetime.now)
    receipt_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    company_name = models.CharField("회사명", max_length=100)
    sourcing = models.CharField("Sourcing", max_length=20, null=True)
    company_field = models.CharField("사업영역", max_length=100, null=True)
    memo = models.TextField("메모", null=True)
    is_invest = models.BooleanField("투자진행", default=False)

    def __str__(self):
        return self.receipt_date.strftime("%Y-%m-%d") + " " + self.company_name

    def get_username(self):
        rname = ''
        for ru in self.receipt_user.all():
            rname = rname + ru.username + '/'
        return rname[:-1]


class ReviewList(models.Model):
    receipt_id = models.ForeignKey(ReceiptList, on_delete=models.CASCADE, related_name='receipt_review')
    review_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    review_detail = models.TextField("세부사항", null=True)
    is_acctive = models.BooleanField("진행여부", default=True)

    def __str__(self):
        return self.receipt_id.company_name