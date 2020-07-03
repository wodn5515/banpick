from django.urls import path

from . import views

app_name = 'draft'

urlpatterns = [
    #   입장
    path('entry/<str:room_id>', views.draft_entry, name='draft_entry'),
    #   방
    path('room/<str:room_id>', views.draft_room, name='draft_room'),
    #   방 생성 결과창
    path('result', views.draft_result, name="draft_result"),
    #   밴픽 GET / POST 
    path('draft/<str:room_id>', views.draft_draft, name="draft_draft"),
    #   챔피언 GET / POST
    path('champion', views.draft_champion, name="draft_champion"),
    #   라인선택 완료
    path('lane/<str:room_id>', views.draft_lane, name="draft_lane")
]