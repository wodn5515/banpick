from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .choices import MODE_CHOICES

# Create your models here.

class Draft(models.Model):
    
    class Meta:
        verbose_name = ('밴픽')
        verbose_name_plural = ('밴픽')

    mode = models.CharField(
        verbose_name="모드", max_length=20, choices=MODE_CHOICES, default='1'
    )

    match_name = models.CharField(
        verbose_name='매치 이름', max_length=255
    )

    code = models.CharField(
        verbose_name='방 코드', unique=True, null=True, max_length=255
    )

    password = models.CharField(
        verbose_name='패스워드', max_length=255
    )

    blue_team_name = models.CharField(
        verbose_name='블루팀 팀명', max_length=255
    )

    blue_player_name = models.CharField(
        verbose_name='블루팀 플레이어명', default='', max_length=100
    )

    red_team_name = models.CharField(
        verbose_name='레드팀 팀명', max_length=255
    )

    red_player_name = models.CharField(
        verbose_name='레드팀 플레이어명', default='', max_length=100
    )

    banpick = models.CharField(
        verbose_name='밴픽Data', max_length=255, blank=True
    )

    banpick_final = models.CharField(
        verbose_name='밴픽최종', max_length=255, blank=True, default=""
    )

    blue_done = models.BooleanField(
        verbose_name='블루팀 라인', default=False
    )

    red_done = models.BooleanField(
        verbose_name='레드팀 라인', default=False
    )

    timer = models.DateTimeField(
        verbose_name="시작", blank=True, null=True
    )

    date = models.DateTimeField(
        verbose_name="일시", default=timezone.now
    )
    
    def __str__(self):
        return f'{self.match_name}'

    def entry_url(self):
        return f'/draft/entry/{self.code}'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class Champion(models.Model):

    class Meta:
        verbose_name = ('챔피언')
        verbose_name_plural = ('챔피언')

    no = models.CharField(verbose_name='챔피언번호', max_length=3, default='')
    name = models.CharField(verbose_name='챔피언명', max_length=20, default='', help_text='한글로 입력해주세요. ex)가렌')
    lane = models.CharField(verbose_name='라인', max_length=20, default='', help_text='한글로 입력해주세요. ex)탑/미드')
    keyword = models.CharField(verbose_name="검색키워드", max_length=20, default="")

    def __str__(self):
        return f'{self.name}'