import itertools
import random

from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404, render

from .models import Team, Player, Matches, Points


def _paginate(object_list, request):
    obj_paging = Paginator(object_list, 20)
    page = request.GET.get("page")
    paged_objects = obj_paging.get_page(page)
    return paged_objects


def index(request):

    points = Points.objects.all()
    matches_list = Matches.objects.all()
    matches = _paginate(matches_list, request)
    context = {
        'matches': matches,
        'points': points
    }
    return render(request, 'index.html', context)


def teams_index(request):
    teams = Team.objects.order_by('name')
    teams_list = _paginate(teams, request)
    context = {'teams_list': teams_list}
    return render(request, 'teams/index.html', context)


def teams_detail(request, team_id):

    team = get_object_or_404(Team, pk=team_id)
    context = {'team': team}
    return render(request, 'teams/detail.html', context)


def players_index(request):

    players = Player.objects.order_by('last_name')
    players_list = _paginate(players, request)
    context = {'players_list': players_list}
    return render(request, 'players/index.html', context)


def players_detail(request, player_id):

    player = get_object_or_404(Player, pk=player_id)
    context = {'player': player}
    return render(request, 'players/detail.html', context)


def matches_create(request):

    context = {}
    err_msg = ("Missing or invalid key in your input. You must specify "
               "'match_number' greater than 0, 'match_stadium' less than 256 "
               "chars, 'match_location' less than 256 chars, "
               "'match_tournament' less than 256 chars and exactly two teams "
               "playing.")
    try:
        team_1_name = request.POST['team_1']
        team_2_name = request.POST['team_2']
        match_number = request.POST['match_number']
        if int(match_number) < 1:
            raise KeyError
        match_stadium = request.POST['match_stadium']
        match_location = request.POST['match_location']
        match_tournament = request.POST['match_tournament']
    except KeyError:
        context['error_message'] = err_msg
        return render(request, 'matches/create.html', context)
    else:
        match = Matches(match_number=match_number, match_stadium=match_stadium,
                        match_location=match_location,
                        match_tournament=match_tournament)
        match.save()
        try:
            team_1 = Team.objects.get(name__exact=team_1_name)
            team_2 = Team.objects.get(name__exact=team_2_name)
            match.teams.set([team_1, team_2])
            match.save()
        except Team.DoesNotExist:
            context['error_message'] = ("\nYou specified one of more teams that"
                                        " do not exist in the system. Please "
                                        "try again with valid teams.")
            return render(request, 'matches/create.html', context)
        context['match'] = match
    return render(request, 'matches/created.html', context)


def matches_fixtures_create(request):

    all_teams = Team.objects.all()
    # Create a simple all combination matches fixtures. More sophisticated
    # tournament creation could be another feature.
    match_possibilities = itertools.combinations(all_teams, 2)
    # TODO: add ability to set mutiple stadium, location and tournament.
    # To avoid dependency for this project, package like names to generate
    # random location, etc. names has been avoided. For the scope of this
    # project, sticking to hard coded names should be acceptable
    tournament_no = str(random.randint(1, 999999999999999))
    for combination in match_possibilities:
        while True:
            match = Matches(match_number=random.randint(1, 999999999999999),
                            match_stadium="Stadium",
                            match_location="Location",
                            match_tournament=("Tournament " + tournament_no))
            try:
                match.save()
                break
            except IntegrityError:
                continue
        match.teams.set(list(combination))
        match.save()

    return render(request, 'matches/tournament_created.html',
                  {'tournament_no': tournament_no})


def matches_detail(request, match_id):

    match = get_object_or_404(Matches, pk=match_id)
    context = {'match': match}
    return render(request, 'matches/detail.html', context)