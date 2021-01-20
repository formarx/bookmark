from django.db import models
from django.db.models import Q
from django.urls import reverse

from core.models import TimeStampedModel
#from accounts.models import Account
from django.conf import settings

class Board(models.Model):
    def __str__(self):
        return 'Board Name: ' + self.name

    def get_absolute_url(self):
        return reverse('board:post_list', args=[self.slug])

    slug = models.CharField(default='', unique=True, max_length=100)
    name = models.CharField(default='', max_length=100)
    posts_chunk_size = models.IntegerField(default=10)
    post_pages_nav_chunk_size = models.IntegerField(default=10)
    comments_chunk_size = models.IntegerField(default=5)
    comment_pages_nav_chunk_size = models.IntegerField(default=10)


class PostQuerySet(models.QuerySet):
    def search(self, search_flag, query):
        if search_flag == 'TITLE':
            return self.filter(title__contains=query)
        elif search_flag == 'CONTENT':
            return self.filter(content__contains=query)
        elif search_flag == 'BOTH':
            return self.filter(Q(title__contains=query) | Q(content__contains=query))
        else:
            return self.all()

    def remain(self):
        return self.filter(is_deleted=False)

    def board(self, board):
        return self.filter(board=board)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def search(self, search_flag, query):
        return self.get_queryset().search(search_flag, query)

    def remain(self):
        return self.get_queryset().remain()

    def board(self, board):
        return self.get_queryset().board(board)


class Post(TimeStampedModel):
    def __str__(self):
        return 'Post Title: ' + self.title

    SEARCH_FLAG = [
        ('TITLE', '제목'),
        ('CONTENT', '내용'),
        ('BOTH', '제목+내용')
    ]

    objects = PostManager()

    title = models.CharField(blank=False, max_length=100)
    content = models.TextField(default='')
    board = models.ForeignKey(Board, null=True, on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)
    page_view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField(null=True, default='')

    def get_absolute_url(self):
        return reverse('board:view_post', args=[self.id])


class EditedPostHistory(TimeStampedModel):
    post = models.ForeignKey(Post, null=False, default=None, on_delete=models.CASCADE)
    title = models.CharField(default='', max_length=100)
    content = models.TextField(default='')
    ip = models.GenericIPAddressField(null=True, default='')


class Attachment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    editedPostHistory = models.ForeignKey(EditedPostHistory, null=True, default=None, on_delete=models.CASCADE)
    attachment = models.FileField(blank=True, null=True)


class Comment(TimeStampedModel):
    content = models.TextField(default='')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.DO_NOTHING)
    ip = models.GenericIPAddressField(null=True, default='')