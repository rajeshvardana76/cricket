from django.contrib import admin

from .models import Team, Player, PlayerHistory, Matches, Points

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(PlayerHistory)
admin.site.register(Matches)
admin.site.register(Points)