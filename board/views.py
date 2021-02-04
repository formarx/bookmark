from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.urls import reverse
from django.db.models import F
from django.contrib.auth.decorators import login_required

from board.models import Post, Board, Comment, EditedPostHistory, Attachment, Approval
#from accounts.models import Account
from board.forms import PostForm, AttachmentForm
from core.utils import get_pages_nav_info, get_ip

@require_GET
@login_required
def home(request):
    boards = Board.objects.all()

    data = []
    for board in boards:
        data.append({
            'board': board,
            'recent_posts': Post.objects.board(board).remain().order_by('-id')[:5]
        })
    return render(request, 'board/home.html', {'home_data': data})

@login_required
def new_post(request, board_slug):
    board = Board.objects.get(slug=board_slug)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        attachment_form = AttachmentForm(request.POST, request.FILES)
        if post_form.is_valid() and attachment_form.is_valid() and request.user.is_authenticated:
            post = post_form.save(commit=False)
            post.board = board
            post.ip = get_ip(request)
            try:
                post.account = request.user
            except Post.DoesNotExist:
                post.account = None
            post.save()
            attachment = attachment_form.save(commit=False)
            attachment.post = post
            attachment.save()
            return redirect(board)
    else:
        post_form = PostForm()
        attachment_form = AttachmentForm()

    return render(request, 'board/new_post.html', {'board': board, 'post_form': post_form, 
        'attachment_form': attachment_form})

@login_required
@require_GET
def post_list(request, board_slug, appr_type='all'):
    board = Board.objects.get(slug=board_slug)

    # search
    search_info = {
        'query': request.GET.get('query', ''),
        'selected_flag': request.GET.get('search_flag', 'TITLE'),
        'flags': Post.SEARCH_FLAG
    }

    if board.is_approval and appr_type != 'all':
        posts = get_appr_list(request, appr_type)
    else:
        if search_info['query']:
            posts = Post.objects.board(board).remain().search(search_info['selected_flag'], 
                search_info['query']).order_by('-id')
        else:
            posts = Post.objects.board(board).remain().order_by('-id')

    # pagination
    paginator = Paginator(posts, board.posts_chunk_size)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(posts, nav_chunk_size=board.post_pages_nav_chunk_size)

    return render(request, 'board/post_list.html', {
        'posts': posts,
        'board': board,
        'pages_nav_info': pages_nav_info,
        'search_info': search_info
    })

@login_required
@require_GET
def view_post(request, post_id):
    non_sliced_query_set = Post.objects.filter(id=post_id)
    non_sliced_query_set.update(page_view_count=F('page_view_count') + 1)

    post = Post.objects.get(id=post_id)
    try:
        attachment = Attachment.objects.get(post=post)
        uploaded_file = attachment.attachment
    except Attachment.DoesNotExist:
        uploaded_file = None

    comments_all_list = Comment.objects.filter(post=post, is_deleted=False).order_by('-id')

    is_modified = False
    history = EditedPostHistory.objects.filter(post=post)
    if history:
        is_modified = True

    paginator = Paginator(comments_all_list, post.board.comments_chunk_size)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments,
        nav_chunk_size=post.board.comment_pages_nav_chunk_size)

    is_authenticated = False
    if post.account == request.user or request.user.is_superuser:
        is_authenticated = True

    is_approval = post.board.is_approval
    appr_list = []
    if is_approval:
        appr_list = Approval.objects.filter(post=post).order_by('appr_priority')

    # search
    appr_info = {
        'query': request.GET.get('query', ''),
        'selected_flag': request.GET.get('search_flag', 'TITLE'),
        'flags': Approval.ApprState.choices
    }

    return render(request, 'board/view_post.html', {
        'post': post,
        'uploaded_file': uploaded_file,
        'is_modified': is_modified,
        'comments': comments,
        'pages_nav_info': pages_nav_info,
        'is_authenticated': is_authenticated,
        'is_approval': is_approval,
        'appr_list': appr_list,
        'appr_info': appr_info,
    })

@login_required
@require_GET
def comment_list(request, post_id):
    post = Post.objects.get(id=post_id)
    comments_all_list = Comment.objects.filter(post=post, is_deleted=False).order_by('-id')

    paginator = Paginator(comments_all_list, post.board.comments_chunk_size)
    page = request.GET.get('page')

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)

    pages_nav_info = get_pages_nav_info(comments,
        nav_chunk_size=post.board.comment_pages_nav_chunk_size)

    return render(request, 'board/comment_list.html', {
        'post': post,
        'comments': comments,
        'pages_nav_info': pages_nav_info
    })

@login_required
@require_GET
def post_history_list(request, post_id):
    post = Post.objects.get(id=post_id)
    post_histories = EditedPostHistory.objects.filter(post=post).order_by('-id')
    history_list = []
    for history in post_histories:
        try:
            attachment = Attachment.objects.get(editedPostHistory=history)
            uploaded_file = attachment.attachment
        except Attachment.DoesNotExist:
            uploaded_file = None
        history_list.append([history, uploaded_file])

    return render(request, 'board/post_history_list.html', {
        'history_list': history_list,
        'post_id': post_id
    })


@login_required
def edit_post(request, post_id):
    origin_post = Post.objects.get(id=post_id)
    edited_post = Post.objects.get(id=post_id)

    if request.user != origin_post.account and not request.user.is_superuser:
        return redirect('/')

    try:
        origin_attachment = Attachment.objects.get(post=origin_post)
        origin_attachment_name = origin_attachment.attachment.name
    except Attachment.DoesNotExist:
        origin_attachment = None
        origin_attachment_name = ''

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=edited_post)
        attachment_form = AttachmentForm(request.POST, request.FILES)

        # origin_attachment_name != request.FILES.get('attachment', ''):
        if not origin_attachment and request.FILES.get('attachment', '') != '' or \
                origin_attachment and request.FILES.get('attachment', '') != '' or \
                request.POST.get('attachment-clear', '') == 'on':
            attach_edit = True
        else:
            attach_edit = False

        if origin_post.title != request.POST['title'] or \
                origin_post.content != request.POST['content'] or attach_edit:

            if post_form.is_valid() and attachment_form.is_valid():
                edited_post.save()

                edited_post_history = EditedPostHistory.objects.create(
                    post=origin_post,
                    title=origin_post.title,
                    content=origin_post.content,
                    ip=origin_post.ip
                )
                edited_post_history.save()

                # add attachment
                if not origin_attachment and request.FILES.get('attachment', '') != '':
                    new_attachment = attachment_form.save(commit=False)
                    new_attachment.post = edited_post
                    new_attachment.save()

                # modify attachment
                elif origin_attachment and request.FILES.get('attachment', '') != '' \
                        and origin_attachment_name != request.FILES.get('attachment', ''):
                    origin_attachment.post = None
                    origin_attachment.editedPostHistory = edited_post_history
                    origin_attachment.save()

                    new_attachment = attachment_form.save(commit=False)
                    new_attachment.post = edited_post
                    new_attachment.save()

                # remove attachment
                elif request.POST.get('attachment-clear', '') == 'on':
                    origin_attachment.post = None
                    origin_attachment.editedPostHistory = edited_post_history
                    origin_attachment.save()

                return redirect(edited_post)
        else:
            error_message = "변경 사항이 없습니다"
            return render(request, 'board/edit_post.html', {
                'post': origin_post,
                'post_form': post_form,
                'attachment_form': attachment_form,
                'error_alert': error_message
            })
    else:
        post_form = PostForm(initial={'title': origin_post.title, 'content': origin_post.content})
        if origin_attachment:
            attachment_form = AttachmentForm(initial={'attachment': origin_attachment.attachment})
        else:
            attachment_form = AttachmentForm()

    return render(request, 'board/edit_post.html',
        {'post': origin_post, 'post_form': post_form, 'attachment_form': attachment_form})


@require_POST
def new_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    content = request.POST['comment_content']
    if request.user.is_authenticated and content != '':
        Comment.objects.create(
            post=post,
            content=content,
            account=request.user,
            ip=get_ip(request)
        )

    return redirect(reverse('board:comment_list', args=[post_id]))


@require_POST
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.account:
        comment.is_deleted = True
        comment.save()

    return redirect(reverse('board:comment_list', args=[post_id]))


@require_POST
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.is_deleted = True
    post.save(update_fields=['is_deleted'])

    return redirect(post.board)


@require_POST
@csrf_exempt
def like_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    post.update(like_count=F('like_count') + 1)

    return HttpResponse(post[0].like_count)

@login_required
@require_POST
@csrf_exempt
def edit_appr(request, post_id):
    post = Post.objects.get(id=post_id)

    is_approval = post.board.is_approval
    appr_list = []
    if is_approval:
        appr_list = Approval.objects.filter(post=post).order_by('appr_priority')

    for appr in appr_list:
        if appr.account == request.user :
            appr_sel = "appr_state-%d" % appr.id
            appr.appr_state = request.POST[appr_sel]
            appr.save()

    return redirect(post)

def get_appr_list(request, appr_type='dd'):
    ## 상신함 draft
    if appr_type[0] == 'd': 
        appr_list = Approval.objects.filter(account=request.user, appr_priority=1).order_by('-id')
    ## 결재함
    elif appr_type[0] == 'a':
        appr_list = Approval.objects.filter(account=request.user, appr_priority__gt=1).order_by('-id')
    ## 수신함
    elif appr_type[0] == 'r':
        appr_list = Approval.objects.filter(account=request.user, appr_line=Approval.ApprLine.RECEIVE).order_by('-id')
    ## 참조함
    elif appr_type == 'cc':
        appr_list = Approval.objects.filter(account=request.user, appr_line=Approval.ApprLine.CARBONCOPY).order_by('-id')
    else:
        return []    

    posts = []
    for appr in appr_list:
        if check_appr(request, appr.post.id, appr_type):
            post = Post.objects.get(id=appr.post.id)
            posts.append(post)

    return posts

def check_appr(request, post_id, appr_type):
    appr_list = Approval.objects.filter(post=post_id, appr_priority__gt=0).order_by('appr_priority')

    appr_max = len(appr_list) - 1

    return_val = False
    if appr_type == 'dd': # 상신한 
        return_val = appr_list[appr_max].appr_state == Approval.ApprState.NOTYET
    elif appr_type == 'dc': # 완료된
        return_val = appr_list[appr_max].appr_state == Approval.ApprState.ACCEPT
    elif appr_type == 'dt': # 저장된
        return_val = appr_list[0].appr_state == Approval.ApprState.NOTYET
    elif appr_type == 'dr': # 반려된
        return_val = appr_list[0].appr_state == Approval.ApprState.RETURN
    #elif appr_type == 'dn': # 반송된
    #elif appr_type == 'de': # 회수된
    ## 결재함
    elif appr_type == 'ab': # 결재전
        appr = Approval.objects.get(post=post_id, account=request.user)
        if appr.appr_state == Approval.ApprState.NOTYET:
            prev_apprs = Approval.objects.filter(post=post_id, appr_priority=appr.appr_priority-1)
            return_val = True
            for prev_appr in prev_apprs:
                if prev_appr.appr_state != Approval.ApprState.ACCEPT:
                    return_val = False
    elif appr_type == 'ai': # 진행중
        appr = Approval.objects.get(post=post_id, account=request.user)
        return_val = appr.appr_state == Approval.ApprState.ACCEPT and appr_list[appr_max].appr_state == Approval.ApprState.NOTYET
    elif appr_type == 'ac': # 완료된
        return_val = appr_list[appr_max].appr_state == Approval.ApprState.ACCEPT
    #elif appr_type == 'ar': # 반려된
    ## 수신함
    elif appr_type == 'rb': # 수신전
        appr = Approval.objects.get(post=post_id, account=request.user)
        return_val = appr.appr_state == Approval.ApprState.NOTYET
    elif appr_type == 'rc': # 완료된
        appr = Approval.objects.get(post=post_id, account=request.user)
        return_val = appr.appr_state == Approval.ApprState.ACCEPT

    return return_val
