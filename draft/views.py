from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Draft, Champion
from .utils import lane_choice_done
import json, datetime
# Create your views here.

def draft_result(request):
    if request.method == 'POST':
        return redirect('home')
    else:
        if not request.session.get('master', False):
            return redirect('home')
        else:
            master = request.session['master']
            draft = Draft.objects.get(pk=master)
            return render(request, 'draft_result.html', {
                'draft': draft
            })

def draft_entry(request, room_code):
    draft = Draft.objects.get(code=room_code)
    if request.method == "POST":
        if draft.mode == "1":
            if request.session.get("master", "") == draft.id:
                password = request.POST.get('password', '')
                if check_password(password, draft.password):
                    request.session['authorized_user' + str(draft.id)] = True
                    return redirect('/draft/room/' + str(draft.code))
                else:
                    messages.info(request, '비밀번호가 일치하지 않습니다.')
                    return render(request, 'draft_entry.html', {
                        'draft': draft
                    })
            messages.info(request, '권한이 없습니다.')
            return render(request, 'draft_entry.html', {
                'draft': draft
            })
        else:
            password = request.POST.get('password', '')
            team = request.POST.get('team', '')
            if team:
                if check_password(password, draft.password):
                    request.session['authorized_user' + str(draft.id)] = True
                    request.session['team'] = team
                    return redirect('/draft/room/' + str(draft.code))
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

def draft_room(request, room_code):
    draft = Draft.objects.get(code=room_code)
    champions = Champion.objects.all().order_by('name')
    team = request.session.get('team', '')
    if not request.session.get("master", False) and draft.mode == "1":
        messages.info(request, '권한이 없습니다.')
        return render(request, 'draft_entry.html', {
            'draft': draft
        })
    if not request.session.get('authorized_user' + str(draft.id), False):
        return redirect('draft:draft_entry', draft.code)
    else:
        return render(request, 'draft_room.html', {
            'draft': draft,
            'champions': champions,
            'team': team
        })

def draft_draft(request, room_code):
    draft = Draft.objects.get(code=room_code)
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        no = data['no']
        if no:
            if draft.banpick:
                draft.banpick += '/'+str(no)
            else:
                draft.banpick += str(no)
        draft.timer = datetime.datetime.now()
        draft.save()
        return HttpResponse('success')
    else:
        data = {}
        if draft.banpick:
            cp_list = list(range(0,148))
            for i in draft.banpick.split('/'):
                if i != '999':
                    cp_list.remove(int(i))
            data['champions_valid'] = cp_list
        if draft.blue_done and draft.red_done:
            data['banpick'] = draft.banpick_final
        else:
            data['banpick'] = draft.banpick
        if draft.timer:
            data['timer'] = int(draft.timer.timestamp())
        if draft.blue_done:
            data['blue_done'] = True
        if draft.red_done:
            data['red_done'] = True
        return JsonResponse(data, safe=False)


def draft_champion(request):
    lane = request.GET.get('lane')
    name = request.GET.get('name')
    code = request.GET.get('code')
    cp_list = []
    banpick = Draft.objects.get(code=code).banpick.split('/')
    champions = Champion.objects.all().order_by('name')
    if name != '':
        champions = champions.filter(name__contains=name)
    if lane != '':
        champions = champions.filter(lane__contains=lane)
    for i in champions:
        temp = {}
        temp['no'] = i.no
        temp['name'] = i.name
        if i.no in banpick:
            temp['disabled'] = True
        cp_list.append(temp)
    return JsonResponse(data=cp_list, safe=False)

@require_POST
def draft_lane(request, room_code):
    draft = Draft.objects.get(code=room_code)
    return HttpResponse(lane_choice_done(request, draft))