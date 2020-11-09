from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
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

def draft_entry(request, room_code):
    draft = Draft.objects.get(code=room_code)
    if request.method == "POST":
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
        champions = champions.filter(keyword__contains=name).order_by('name')
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

@require_POST
def draft_lane(request, room_code):
    draft = Draft.objects.get(code=room_code)
    banpick = (draft.banpick_final.split('/') if draft.banpick_final else draft.banpick.split('/'))
    team = request.POST.get('team')
    od_arr = [] # 픽순 라인 리스트
    cp_arr = [] # 챔피언 번호 리스트
    temp_dic = {} # 픽 임시(픽순)
    bp_f = [] # 픽 최종(라인순)
    team_od = ([6,9,10,17,18] if team == 'blue' else [7,8,11,16,19])
    for i in team_od:
        cp_arr.append(banpick[i])
    for i in range(5):
        od_no = request.POST.get(str(i),'')
        if od_no in od_arr:
            return HttpResponse('error')
        od_arr.append(od_no)
        cnt = 0
    for i in od_arr:
        temp_dic[team_od[int(i)]] = cp_arr[cnt]
        cnt += 1
    for key, value in sorted(temp_dic.items()):
        banpick[key] = value
    draft.banpick_final = '/'.join(banpick)
    if team == 'blue':
        draft.blue_done = True
    if team == 'red':
        draft.red_done = True
    draft.save()
    return HttpResponse('/'.join(bp_f))
