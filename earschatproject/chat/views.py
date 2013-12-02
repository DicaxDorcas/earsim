import json
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from chat.models import Message


@login_required
def index(request):
    request.user.last_login = datetime.now()
    request.user.save()
    template_name = 'chat/index.html'

    u = User.objects.all().exclude(username=request.user.username)

    return render(request, template_name, {"users": u})

# @ensure_csrf_cookie
@login_required
def chat(request, user):
    request.user.last_login = datetime.now()
    request.user.save()
    template_name = 'chat/chat.html'

    try:
        u = User.objects.get(username=user)
    except:
        return redirect('index')
    if u == request.user:
        return redirect('index')
    return render(request, template_name, {"room": u.id, "u": u, "username": request.user.username})
    
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
    request.user.last_login = datetime.now()
    request.user.save()
    if request.method != 'POST':
        raise Http404
    p = request.POST
    
    u = User.objects.get(id=int(p['id']))
    r = Message.objects.filter(to_user__in=[u, request.user], from_user__in=[u, request.user]).order_by('-timestamp')[15]

    return HttpResponse(jsonify({'last_message_id' : r.id}))

@login_required
def receive(request):
    request.user.last_login = datetime.now()
    request.user.save()
    if request.method != 'POST':
        raise Http404
    p = request.POST

    u = User.objects.get(id=int(p['id']))
    r = Message.objects.filter(to_user__in=[u, request.user], from_user__in=[u, request.user], pk__gt=int(p['offset'])).order_by('timestamp')  
    
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
