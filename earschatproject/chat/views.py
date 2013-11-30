import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
# from django.views.decorators.csrf import ensure_csrf_cookie

from chat.models import Message


@login_required
def index(request):
    template_name = 'chat/index.html'

    return render(request, template_name)

# @ensure_csrf_cookie
def chat(request, user):
    template_name = 'chat/chat.html'

    u = User.objects.get(username=user)
 
    return render(request, template_name, {"room": u.id})
    
# AJAX views, used by the chat system.
@login_required
def send(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    u = User.objects.get(id=int(p['id']))
    r = Message.objects.create(to_user=u, from_user=request.user, message=p['message'], type='m')
    return HttpResponse('')

@login_required
def sync(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST
    
    u = User.objects.get(id=int(p['id']))
    r = Message.objects.filter(to_user=u, from_user=request.user).order_by('-timestamp')[0]

    return HttpResponse(jsonify({'last_message_id' : r.id}))

@login_required
def receive(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    u = User.objects.get(id=int(p['id']))
    r = Message.objects.filter(to_user=u, from_user=request.user, pk__gt=int(p['offset'])).order_by('-timestamp')

    return HttpResponse(jsonify(r, ['id','from_user','message','type']))

@login_required
def join(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    return HttpResponse('')


@login_required
def leave(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    return HttpResponse('')

def jsonify(object, fields=None, to_dict=False):
    '''Funcion utilitaria para convertir un query set a formato JSON'''
    try:
        import json
    except ImportError:
        import django.utils.simplejson as json

    out = []

    if type(object) not in [dict,list,tuple] :
        for i in object:
            tmp = {}
            if fields:
                for field in fields:
                    tmp[field] = unicode(i.__getattribute__(field))
            else:
                for attr, value in i.__dict__.iteritems():
                    tmp[attr] = value
            out.append(tmp)
    else:
        out = object

    if to_dict:
        return out
    else:
        return json.dumps(out)
