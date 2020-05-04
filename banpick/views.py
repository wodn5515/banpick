from django.shortcuts import render, redirect
from django.urls import reverse
from draft.forms import RoomCreateForm

def home(request):
    if request.method == 'POST':
        forms = RoomCreateForm(request.POST)
        blue_player = request.POST.get('blue_player_top','') + '//' + request.POST.get('blue_player_jg','') + '//' + request.POST.get('blue_player_mid','') + '//' + request.POST.get('blue_player_adc','') + '//' + request.POST.get('blue_player_sup','')
        red_player = request.POST.get('red_player_top','') + '//' + request.POST.get('red_player_jg','') + '//' + request.POST.get('red_player_mid','') + '//' + request.POST.get('red_player_adc','') + '//' + request.POST.get('red_player_sup','')
        if forms.is_valid():
            new_draft = forms.save(commit=False)
            new_draft.red_player_name = red_player
            new_draft.blue_player_name = blue_player
            new_draft.save()
            request.session['room_id'] = new_draft.id
            request.session['master'] = new_draft.id
            return redirect('draft:draft_result')
    else:
        forms = RoomCreateForm()
        return render(request, 'home.html', {
            'forms': forms
        })
    