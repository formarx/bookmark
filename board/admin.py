from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Board, Approval


class ApprovalInline(admin.TabularInline):
    model = Approval
    can_delete = True
    verbose_name_plural = 'Approval'
    
    def get_extra(self, request, obj=None, **kwargs):
        if obj.board.is_approval and obj.approval_set.count() < 2:
            return 3
        return 0

class PostModelAdmin(SummernoteModelAdmin):
    inlines = (ApprovalInline,)

admin.site.register(Post, PostModelAdmin)
admin.site.register(Board)
