from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import CommentForm
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag

# Create your views here.
def post_list(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2)
    page_num=request.GET.get('page')
    try:
        post_list=paginator.page(page_num)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_detail=paginator.page(paginator.num_pages)
    return render(request,'test/post_list.html',{'post_list':post_list,'tag':tag})

def post_detail(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method == 'POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'test/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})

from django.core.mail import send_mail
from .forms import EmailSendForm

def mail_send(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method == 'POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) recommonds read to you "{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read post at:\n{} \n\n{}\'s Comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'manavallu4@gmail.com',['hellosony2244@gmail.com'],)
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'test/shareemail.html',{'form':form,'post':post,'sent':sent})
