# https://woolbro.tistory.com/36

import pandas as pd
from datetime import datetime as dd

from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import *

ex_file = './deallist/deallist.xlsx'

df = pd.read_excel(ex_file, header=1, usecols='B:I')

def get_date(str1, str2):
    year = str1[0:4]
    year = int(year)
    month = str2.split()[0]
    month = month[0: len(month)-1]
    month = int(month)
    week = str2.split()[1]
    week = int(week[0: len(week)-1])
    s = f'{year:04d}-{month:02d}-01'
    first_day = dd.strptime(s, '%Y-%m-%d')
    first_week = first_day.weekday()
    if first_week == 0:
        day = week*7 - 6
    else:
        day = week*7 - first_week + 1
    
    return dd(year, month, day)


def dump(req):
    for i in range(0, len(df)):
        year = df.iloc[i, 0]
        _week = df.iloc[i, 1]
        username = df.iloc[i, 2]
        company_name = df.iloc[i, 3]
        sourcing = df.iloc[i, 4]
        company_field = df.iloc[i, 5]
        memo = df.iloc[i, 6]
        memo1 = df.iloc[i, 7]

        if type(year) == type("STR"):
            date = get_date(year, _week).date()
        else:
            break

        if type(memo) != type("STR"):
            memo = ""

        if type(memo1) == type("STR"):
            memo = memo + " " + memo1

        username = username.split('/')[0]
        uu = User.objects.filter(username=username)[0]
        print(uu.id)
 
        '''    
        receipt_date = models.DateField("접수날짜", default=datetime.datetime.now)
        receipt_user = models.ManyToManyField(settings.AUTH_USER_MODEL)
        company_name = models.CharField("회사명", max_length=100)
        sourcing = models.CharField("Sourcing", max_length=20, null=True)
        company_field = models.CharField("사업영역", max_length=100, null=True)
        memo = models.TextField("메모", null=True)
        is_invest = models.BooleanField("투자진행", default=False)
        '''   
        rr = ReceiptList()
        rr.receipt_date = date
        rr.company_name = company_name
        rr.sourcing = sourcing
        rr.company_field = company_field
        rr.memo = memo
        rr.save()

        rr.receipt_user.add(uu)
        rr.save()

        print(rr.id)



    return redirect('/deallist')


