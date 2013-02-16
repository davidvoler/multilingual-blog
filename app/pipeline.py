from django.http import HttpResponseRedirect

    
def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
       kwargs.get('user') is None:
        return HttpResponseRedirect('/form/')


def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        #if kwargs.get('email'):
        #    username=kwargs['email']
        #else:
        #    username='user%d'%get_next_user_num()
        username = request.session.get('saved_username')
    return {'username': username}


def redirect_to_form2(*args, **kwargs):
    if not kwargs['request'].session.get('saved_first_name'):
        return HttpResponseRedirect('/form2/')


def first_name(request, *args, **kwargs):
    if 'saved_first_name' in request.session:
        user = kwargs['user']
        user.first_name = request.session.get('saved_first_name')
        user.save()
