from datetime import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import TodoList, TodoProject
from .forms import TodoForm

# Create your views here.
class Todo_ListView(generic.TemplateView):
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
            'pcode': pcode,
        })

class Todo_DetailView(generic.DetailView):
    model = TodoList
    template_name = 'todo/todo_detail.html'
    context_object_name = 'todo_list'

class Todo_UpdateView(generic.UpdateView):
    model = TodoList
    template_name = "todo/todo_update.html"
    form_class = TodoForm

    def get_success_url(self):
        return reverse_lazy('doto:list', kwargs={'pcode': self.object.pcode.id })

    def form_valid(self, form):
        form.save()
        return render(self.request, 'todo/todo_success.html', {
            'message': '일정을 업데이트 했습니다', 'pcode': self.object.pcode.id})

class Todo_DeleteView(generic.DeleteView):
    model = TodoList
    success_url = '/todo/'
    context_object_name = 'todo_list'
    template_name = "todo/todo_confirm_delete.html"

def check_post(request, pcode):
    template_name = 'todo/todo_success.html'
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            message = '일정을 추가하였습니다'
            if len(request.POST.get('title')) < 2:
                message = '제목은 2글자 이상으로 입력해주세요'
            else:
                todo = form.save(commit=False)
                todo.pcode = TodoProject.objects.get(id=pcode)
                todo.todo_save()
            return render(request, template_name, {'message': message, 'pcode': pcode})
    else :
        template_name = 'todo/todo_insert.html'
        form = TodoForm
        return render(request, template_name, {'form': form, 'pcode': pcode})

    return render(request, template_name)

def checkbox_event(pk, is_check):
    todo_selected = TodoList.objects.get(id=pk)
    if is_check:
        todo_selected.is_complete = True
        todo_selected.priority = None
    else :
        todo_selected.is_complete = False
    
    todo_selected.save()
    return_value = {'text': '저장되었습니다'}
    return return_value
