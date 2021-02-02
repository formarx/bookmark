from django.db import models
from django.db.models import Max
from django.conf import settings

# Create your models here.
class TodoProject(models.Model):
    pname = models.CharField(max_length=100)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.pname

class TodoList(models.Model):
    pcode = models.ForeignKey(TodoProject, on_delete=models.CASCADE)
    title = models.CharField(blank=False, max_length=100)
    content = models.TextField(default='')
    is_complete = models.BooleanField(default=False)
    priority = models.IntegerField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def todo_save(self):
        self.is_complete = False
        if TodoList.objects.filter(pcode=self.pcode).aggregate(Max('priority'))['priority__max'] is None:
            self.priority = 1
        else:
            self.priority = int(TodoList.objects.filter(pcode=self.pcode).latest('priority').priority) + 1
        self.save()

    def todo_update(self, complete):
        self.is_complete = complete
        self.save()
