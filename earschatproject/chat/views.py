import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
# from django.views.decorators.csrf import ensure_csrf_cookie

from chat.models import Room, Message


@login_required
def index(request):
    template_name = 'chat/index.html'

    return render(request, template_name)

# @ensure_csrf_cookie
def chat(request, user):
    template_name = 'chat/chat.html'
    
    user = User.objects.get(username=user)
    users = []
    users.append(request.user.id)
    users.append(user.id)

    room, created = Room.objects.get_or_create(user_list__id__in=users)
    
    return render(request, template_name, {"room": room.id})
    
# AJAX views, used by the chat system.
@login_required
def send(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    r = Room.objects.get(id=int(p['id']))

    r.say(request.user, p['message'])
    return HttpResponse('')

@login_required
def sync(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST
    
    r = Room.objects.get(id=int(p['id']))

    last_message_id = r.last_message_id()

    return HttpResponse(jsonify({'last_message_id' : last_message_id}))

@login_required
def receive(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    r = Room.objects.get(id=int(p['id']))

    try:
        offset = int(p['offset'])
    except:
        offset = 0

    messages = r.messages(offset)

    return HttpResponse(jsonify(messages, ['id','author','message','type']))

@login_required
def join(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    r = Room.objects.get(id=int(p['id']))
    
    r.join(request.user)
    
    return HttpResponse('')


@login_required
def leave(request):
    if request.method != 'POST':
        raise Http404
    p = request.POST

    r = Room.objects.get(id=int(p['id']))
    
    r.leave(request.user)

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
