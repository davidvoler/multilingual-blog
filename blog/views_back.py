from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from blog.forms import PostForm,PublishPostForm
from blog.models import Post
from blog import *


def index(request):
    posts=Post.objects.filter(published=PUBLISHED)
    return render_to_response('index.html',
                              {'posts':posts},
                              context_instance =  RequestContext(request)) 

@login_required
def my_posts(request):
    posts=Post.objects.filter(author=request.user)
    return render_to_response('my_posts.html',
                              {'posts':posts},
                              context_instance =  RequestContext(request)) 
@login_required
def add_post(request,blog):
    post=Post(author=request.user)
    form=PostForm(data=request.POST or None, instance=post)
    if form.is_valid():
        post=form.save()
        return HttpResponseRedirect('/blog/preview/%d/'%post.id)
    return render_to_response('blog/edit_post.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 
@login_required
def edit_post(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()
    form=PostForm(data=request.POST or None, instance=post)
    if form.is_valid():
        post=form.save()
        return HttpResponseRedirect('/blog/post/preview/%d/'%post.id)
    return render_to_response('blog/edit_post.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 

def view_post(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    return render_to_response('blog/post.html',
                              {'post':post,},
                              context_instance =  RequestContext(request)) 
        
@login_required
def preview_post(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()
    form=PublishPostForm(data=request.POST or None, instance=post)
    if form.is_valid():
        post=form.save()
        return HttpResponseRedirect('/blog/view_post/%d/'%post.id)
    return render_to_response('blog/edit_post.html',
                              {'form':form,
                               'post':post},
                              context_instance =  RequestContext(request)) 
@login_required
def delete_post(request,post_id):
    post=get_object_or_404(Post,pk=post_id)
    if post.author != request.user:
        return HttpResponseForbidden()
    form=PostForm(data=request.POST or None, instance=post)
    if form.is_valid():
        post=form.save()
        return HttpResponseRedirect('/blog/%s/'%post.slug)
    return render_to_response('blog/delete_post.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 
