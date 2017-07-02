from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from ..login.models import User
from .models import Poke


# Create your views here.
def index(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('auth:index')

    user = User.objects.get(id=request.session.get('id'))
    users = User.objects.all()
    pokes = Poke.objects.all()
    pokings = pokes.all().filter(pokee_id=user.id).count()
    pokers = []
    poker_names = []
    for p in pokes:
        if p.pokee_id == user.id:
            if p.poker_id not in pokers:
                pokers.append(p.poker_id)

    for u in pokers:
        poker_names.append(users.get(id=u))

    context = {
        'user': user,
        'users': users,
        'pokers': poker_names,
        'pokes': pokes,
    }
    return render(request, 'pb/index.html', context)


def poke(request):
    if not request.session.get('id'):
        messages.error(request, 'Access Denied. Log in first.')
        return redirect('auth:index')

    poker_id = request.session['id']
    results = Poke.objects.addPoke(request.POST, poker_id)

    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)

    return redirect('pb:index')