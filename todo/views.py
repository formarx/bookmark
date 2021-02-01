from datetime import datetime
from django.shortcuts import render
from django.views import generic

from .models import TodoList

# Create your views here.
class Todo_list(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        if kwargs.__contains__('pcode'):
            pcode = int(kwargs['pcode'])
        else:
            pcode = 1
        
        template_name = 'todo/todo_list.html'
        # 기한 없는 일정
        todo_list_no_endDate = TodoList.objects.filter(pcode=pcode,end_date__isnull=True, is_complete=0).\
            order_by('priority')
        # 기한 있고 마감이 안된 일정
        todo_list_endDate_non_complete = TodoList.objects.filter(pcode=pcode,end_date__isnull=False, is_complete=False).\
            order_by('priority')
        # 마감 된 일정
        todo_list_endDate_complete = TodoList.objects.filter(pcode=pcode,is_complete=True).order_by('priority')
        today = datetime.now()

        close_end_day, over_end_day = [],[]
        for i in todo_list_endDate_non_complete:
            e_day = str(i.end_date).split('-')
            end_day = datetime(int(e_day[0]), int(e_day[1]), int(e_day[2]))
            if (end_day - today).days < -1: 
                over_end_day.append(i.title)
            if (end_day - today).days >= -1 and (end_day - today).days < 3: 
                close_end_day.append(i.title)
        
        return render(request, template_name, {
            'todo_list_endDatea_non_complete': todo_list_endDate_non_complete,
            'todo_list_endDate_complete': todo_list_endDate_complete,
            'todo_list_no_endDate': todo_list_no_endDate,
            'close_end_day': close_end_day,
            'over_end_day': over_end_day,
        })

def check_post(request):
    template_name = 'todo/todo_list.html'

    return render(request, template_name)
    