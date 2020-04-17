from django.db import models
from django.utils import timezone

# Create your models here.

class Draft(models.Model):
    
    class Meta:
        verbose_name = ('밴픽')
        verbose_name_plural = ('밴픽')

    match_name = models.CharField(verbose_name='매치 이름', max_length=255)
    red_team_name = models.CharField(verbose_name='레드팀 팀명', max_length=255)
    blue_team_name = models.CharField(verbose_name='블루팀 팀명', max_length=255)
    password = models.CharField(verbose_name='패스워드', max_length=255)
    banpick = models.CharField(verbose_name='밴픽Data', max_length=255, blank=True)
    timer = models.DateTimeField(verbose_name="시작", blank=True, null=True)
    date = models.DateTimeField(verbose_name="일시", default=timezone.now)

    def __str__(self):
        return f'{self.match_name}'

    def entry_url(self):
        return f'/draft/entry/{self.id}'



class Champion(models.Model):

    class Meta:
        verbose_name = ('챔피언')
        verbose_name_plural = ('챔피언')

    lane = models.CharField(verbose_name='라인', max_length=20, default='', help_text='한글로 입력해주세요. ex)탑/미드')
    keyword = models.CharField(verbose_name='검색어', max_length=255, default='', help_text='"/" 로 구분해주세요. ex)가렌/garen')
    no = models.CharField(verbose_name='챔피언번호', max_length=3, default='')
    name = models.CharField(verbose_name='챔피언명', max_length=20, default='', help_text='한글로 입력해주세요. ex)가렌')

    def __str__(self):
        return f'{self.name}'