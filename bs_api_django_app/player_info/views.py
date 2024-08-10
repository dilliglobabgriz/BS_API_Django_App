from django.http import HttpResponse
from django.template import loader
from .models import Player
from player_info.api.make_requests import Api_Request
from typing import List

def player_info(request):
    myplayers = Player.objects.all().values()
    template = loader.get_template('all_players.html')
    context = {
        'myplayers': myplayers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id: int):
    playerapi = Api_Request()
    try:
        myplayer = Player.objects.get(id=id)
    except Player.DoesNotExist:
        myplayer = None
    playerapi.set_player_tag(myplayer.player_id)
    template = loader.get_template('details.html')
    context = {
        'myplayer': myplayer,
        'playerapi': playerapi,
    }
    return HttpResponse(template.render(context, request))

def details_general(request, id: str):
    playerapi = Api_Request()
    playerapi.set_player_tag(id)
    template = loader.get_template('details_general.html')
    context = {
        'playerapi': playerapi,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def top_global(request):
    try:   
        rankingsapi = Api_Request()
        players: List[str] = rankingsapi.get_leaderboard_player_tags()
    except UnicodeDecodeError as e:
        return HttpResponse(f'Encoding error: {str(e)}, status = 500')
    except Exception as e:
        players = []
        #print(f'Error occurred: {str(e)}')
        
    # Remove leading "#"
    # Should add formatting method to ApiRequests
    formatted_players = [s[1:] for s in players]

    player_names: List[str] = []
    for player in formatted_players:
        rankingsapi.set_player_tag(player)
        player_names.append(rankingsapi.get_gamer_tag())

    template = loader.get_template('top_global.html')
    context = {
        'rankingsapi': rankingsapi,
        'players': formatted_players,
        'player_names': player_names,
    }
    return HttpResponse(template.render(context, request))

def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))