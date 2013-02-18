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

from blog.forms import *
from blog.models import Blog,Entry


def index(request):
    entries=Entry.objects.filter(deleted=False,published=True)
    blogs=Blog.objects.filter(deleted=False)
    return render_to_response('index.html',
                              {'entries':entries,
                               'blogs':blogs},
                              context_instance =  RequestContext(request)) 


def blog(request,slug):
    blog=get_object_or_404(Blog,slug=slug)
    deleted=False
    published=True
    if blog.has_edit_permision(request.user):
        #show deleted an unpublished entries
        deleted=request.GET.get('deleted',False)
        #published=request.GET.get('published',True)
        entries=Entry.objects.filter(blog=blog,deleted=deleted)
    else:   
        entries=Entry.objects.filter(blog=blog,published=published,deleted=deleted)
    return render_to_response('blog/blog.html',
                              {'blog':blog,
                               'entries':entries,
                               'edit_permision':blog.has_edit_permision(request.user)},
                              context_instance =  RequestContext(request)) 
def blogs(request):
    user=request.GET.get('user','')
    lang=request.GET.get('lang','')
    
    blogs=Blog.objects.all()
    if user:
        blogs=blogs.filter(owner=user)
    if lang:
        blogs=blogs.filter(lang=lang)

    #PAGINATOR
    return render_to_response('blog/blogs.html',
                              {'blogs':blogs},
                              context_instance =  RequestContext(request)) 

@login_required
def add_blog(request):
    blog=Blog(owner=request.user)
    form=BlogForm(data=request.POST or None, instance=blog)
    if form.is_valid():
        blog=form.save()
        return HttpResponseRedirect('/blog/blog/%s/'%blog.slug)
    return render_to_response('blog/edit_blog.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 
@login_required
def edit_blog(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    if not blog.has_edit_permision(request.user):
        return HttpResponseForbidden()
    form=BlogForm(data=request.POST or None, instance=blog)
    if form.is_valid():
        blog=form.save()
        return HttpResponseRedirect('/blog/blog/%s/'%blog.slug)
    return render_to_response('blog/edit_blog.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 
@login_required
def delete_blog(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    if not blog.has_edit_permision(request.user):
        return HttpResponseForbidden()
    form=BlogDeleteForm(data=request.POST or None, instance=blog)
    if form.is_valid():
        blog=form.save()
        return HttpResponseRedirect('/blog/blogs/?user=%s'%request.user.pk)
    return render_to_response('blog/delete_blog.html',
                              {'form':form,
                               'blog':blog},
                              context_instance =  RequestContext(request)) 

@login_required
def add_entry(request,blog_id):
    blog=get_object_or_404(Blog,pk=blog_id)
    if not blog.has_edit_permision(request.user):
        return HttpResponseForbidden()
    entry=Entry(blog=blog,lang=blog.lang,author=request.user)
    form=EntryForm(data=request.POST or None, instance=entry)
    if form.is_valid():
        entry=form.save()
        return HttpResponseRedirect('/blog/entry/%s/'%entry.slug)
    return render_to_response('blog/edit_entry.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 

@login_required
def edit_entry(request,entry_id):
    entry=get_object_or_404(Entry,pk=entry_id)
    if not entry.has_edit_permision(request.user):
        return HttpResponseForbidden()
    form=EntryForm(data=request.POST or None, instance=entry)
    if form.is_valid():
        entry=form.save()
        return HttpResponseRedirect('/blog/entry/%s/'%entry.slug)
    return render_to_response('blog/edit_entry.html',
                              {'form':form,},
                              context_instance =  RequestContext(request)) 

@login_required
def delete_entry(request,entry_id):
    entry=get_object_or_404(Entry,pk=entry_id)
    if not entry.has_edit_permision(request.user):
        return HttpResponseForbidden()
    form=EntryDeleteForm(data=request.POST or None, instance=entry)
    if form.is_valid():
        entry=form.save()
        return HttpResponseRedirect('/blog/blog/%s/'%entry.blog.slug)
    return render_to_response('blog/delete_entry.html',
                              {'form':form,
                               'entry':entry},
                              context_instance =  RequestContext(request)) 

def entry(request,slug):
    entry=get_object_or_404(Entry,slug=slug)
    return render_to_response('blog/entry.html',
                              {'entry':entry},
                              context_instance =  RequestContext(request)) 

@login_required
def trnaslate_entry(request,entry_id,lang):
    entry=get_object_or_404(Entry,pk=entry_id)
    trans=Entry(author=request.user,
                lang=lang,
                translated_from=entry,
                blog=entry.blog)
    form=EntryForm(data=request.POST or None, instance=trans)
    if form.is_valid():
        trans=form.save()
        return HttpResponseRedirect('/blog/entry/%s/'%trans.slug)
    return render_to_response('blog/translate_entry.html',
                              {'form':form,
                               'entry':entry,
                               'lang':lang},
                              context_instance =  RequestContext(request)) 

