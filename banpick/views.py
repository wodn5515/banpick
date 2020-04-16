from django.shortcuts import render, redirect
from django.urls import reverse
from draft.forms import RoomCreateForm

def home(request):
    if request.method == 'POST':
        forms = RoomCreateForm(request.POST)
        if forms.is_valid():
            new_draft = forms.save()
            request.session['room_id'] = new_draft.id
            request.session['master'] = new_draft.id
            return redirect('draft:draft_result')
    else:
        forms = RoomCreateForm()
        return render(request, 'home.html', {
            'forms': forms
        })
    