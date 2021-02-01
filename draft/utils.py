from django.http import HttpResponse

def lane_choice_done(request, draft):
    banpick = (draft.banpick_final.split('/') if draft.banpick_final else draft.banpick.split('/'))
    team = request.POST.get("team",None)
    team_od = (([6,9,10,17,18] if team == "blue" else [7,8,11,16,19]) if team else [6,9,10,17,18,7,8,11,16,19])
    cp_arr = [] # 챔피언 번호 리스트
    for i in team_od:
        cp_arr.append(banpick[i])
    if team:
        cnt = 0
        od_arr = [] # 픽순 라인 리스트
        temp_dic = {} # 픽 임시(픽순)
        for i in range(5):
            od_no = request.POST.get(str(i),'')
            if od_no in od_arr:
                return 'error'
            od_arr.append(od_no)
        for i in od_arr:
            temp_dic[team_od[int(i)]] = cp_arr[cnt]
            cnt += 1
        for key, value in sorted(temp_dic.items()):
            banpick[key] = value
    else:
        cnt = 0
        for i in range(2):
            od_arr = [] # 픽순 라인 리스트
            temp_dic = {} # 픽 임시(픽순)
            for j in range(5):
                od_no = request.POST.get(str((i*5)+j),'')
                if od_no in od_arr:
                    return "error/" + str(i)
                od_arr.append(od_no)
            for k in od_arr:
                temp_dic[team_od[(5*i)+int(k)]] = cp_arr[cnt]
                cnt += 1
            for key, value in sorted(temp_dic.items()):
                banpick[key] = value
    draft.banpick_final = '/'.join(banpick)
    if team:
        if team == 'blue':
            draft.blue_done = True
        if team == 'red':
            draft.red_done = True
    else:
        draft.blue_done = True
        draft.red_done = True
    draft.save()
    return "pass"