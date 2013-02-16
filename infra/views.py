from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from infra.models import Language
from infra.forms import ProfileForm
from perm.http import Http403

@login_required
def edit_profile(request):
    prof=request.user.profile
    form=ProfileForm(data=request.POST or None, instance=prof)
    if form.is_valid():
        form.save()
        #TODO: save other elements like user languages
    return render_to_response('infra/edit_p.html',
                              {'form':form,
                               },
            context_instance =  RequestContext(request)) 

    
        
def change_lang(request,lang,learn):
    
    if learn=='0':
        learning=False
    else:
        learning=True
    
    if request.user.is_authenticated():
        request.user.profile.set_lang(lang,learning)
        res=lang
    else:
        try:
            language=Language.objects.get(pk=lang)
        except:
            language=None
        if learning:
            request.session['lang'] = language
        else:
            request.session['d_lang'] = language
        res=lang
    return HttpResponse(res, mimetype="application/javascript")

@login_required
def moderate_spam(request,lang,exp_lang,domain):
    if not domain.has_domain_perms(request.user,'moderate',lang,exp_lang,domain ):
        raise Http403('User is not allowed to moderate domain')
    """
    in the html
    List user's elements that are defiend as spam. (with limit 15 example + view all)
    list user's elemets that are not defiend as spam (with limit like above)
    Moderator can block user. unset cards as spam.
    
    SuperUser + Moderator can moderate the non member domains
    owners can moderate the their own domains
    SuperUser can define a domain as spam
     
    
    """
    return render_to_response('infra/moderate_users.html',
                              {},
            context_instance =  RequestContext(request)) 
   