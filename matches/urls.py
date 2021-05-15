from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('teams/', views.teams_index, name='teams_index'),
    path('teams/<uuid:team_id>/', views.teams_detail, name='teams_detail'),
    path('players/', views.players_index, name='players_index'),
    path('players/<uuid:player_id>/', views.players_detail, name='players_detail'),
    path('matches/', views.matches_create, name='matches_create'),
    path('matches/fixtures', views.matches_fixtures_create, name='fixtures_create'),
    path('matches/<uuid:match_id>/', views.matches_detail, name='matches_detail')
]