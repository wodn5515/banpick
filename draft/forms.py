from django import forms
from .models import Draft

class RoomCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RoomCreateForm, self).__init__(*args, **kwargs)
    
    match_name = forms.CharField(
        label="매치명",
        widget=forms.TextInput(attrs={
            'class': 'bg_black bold draft_input',
            'autofocus': 'true',
            'onkeyup': 'submitable()'
        })
    )

    blue_team_name = forms.CharField(
        label="블루팀 팀명",
        help_text="<span class='f_right player_check'><input id='blue_player_check' class='blue' type='checkbox' onchange='playerCheck(event);'><label for='blue_player_check'>플레이어 입력하기</label></span>",
        widget=forms.TextInput(attrs={
            'class': 'bg_blue bold draft_input',
            'onkeyup': 'submitable()'
        })
    )

    red_team_name = forms.CharField(
        label="레드팀 팀명",
        help_text="<span class='f_right player_check'><input id='red_player_check' class='red' type='checkbox' onchange='playerCheck(event);'><label for='red_player_check'>플레이어 입력하기</label></span>",
        widget=forms.TextInput(attrs={
            'class': 'bg_red bold draft_input',
            'onkeyup': 'submitable()'
        })
    )

    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput(attrs={
            'class': 'bg_black bold draft_input',
            'onkeyup': 'submitable()'
        })
    )

    class Meta:
        model = Draft
        fields = ('match_name', 'blue_team_name', 'red_team_name', 'password')

    def save(self, commit=True):
        draft = super().save(commit=False)
        draft.set_password(self.cleaned_data["password"])
        if commit:
            draft.save()
        return draft