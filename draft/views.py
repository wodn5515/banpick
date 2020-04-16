from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from .models import Draft, Champion
import json, datetime
# Create your views here.

def draft_result(request):
    if request.method == 'POST':
        return redirect('home')
    else:
        if not request.session.get('room_id', False):
            return redirect('home')
        else:
            room_id = request.session['room_id']
            draft = Draft.objects.get(pk=room_id)
            return render(request, 'draft_result.html', {
                'draft': draft
            })

def draft_entry(request, room_id):
    draft = Draft.objects.get(pk=room_id)
    if request.method == "POST":
        password = request.POST.get('password', '')
        team = request.POST.get('team', '')
        if team:
            if password == draft.password:
                request.session['authorized_user' + str(draft.id)] = True
                request.session['team'] = team
                return redirect('/draft/room/' + str(draft.id))
            else:
                messages.info(request, '비밀번호가 일치하지 않습니다.')
                return render(request, 'draft_entry.html', {
                    'draft': draft,
                    'team': team
                })
        else:
            messages.info(request, '팀을 선택해주세요.')
            return render(request, 'draft_entry.html', {
                'draft': draft,
                'team': team
            })
    else:
        return render(request, 'draft_entry.html', {
            'draft': draft
        })

def draft_room(request, room_id):
    draft = Draft.objects.get(pk=room_id)
    champions = Champion.objects.all().order_by('name')
    team = request.session.get('team', '')
    if not request.session.get('authorized_user' + str(draft.id), False):
        return redirect('draft:draft_entry', draft.id)
    else:
        return render(request, 'draft_room.html', {
            'draft': draft,
            'champions': champions,
            'team': team
        })

def draft_draft(request, room_id):
    draft = Draft.objects.get(pk=room_id)
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        no = data['no']
        if draft.banpick:
            draft.banpick += '/'+str(no)
        else:
            draft.banpick += str(no)
        draft.timer = datetime.datetime.now()
        draft.save()
        return HttpResponse('success')
    else:
        data = {}
        data['banpick'] = draft.banpick
        if draft.timer:
            data['start'] = int(draft.timer.timestamp())
        return JsonResponse(data, safe=False)


def draft_champion(request):
    lane = request.GET.get('lane')
    name = request.GET.get('name')
    draft = request.GET.get('draft')
    cp_list = []
    banpick = Draft.objects.get(pk=draft).banpick.split('/')
    champions = Champion.objects.all().order_by('name')
    if name != '':
        champions = champions.filter(name__contains=name).order_by('name')
    if lane != '':
        champions = champions.filter(lane=lane).order_by('name')
    for i in champions:
        temp = {}
        temp['no'] = i.no
        temp['name'] = i.name
        if i.no in banpick:
            temp['disabled'] = True
        cp_list.append(temp)
    return JsonResponse(data=cp_list, safe=False)
