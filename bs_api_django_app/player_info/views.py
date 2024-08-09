from django.http import HttpResponse
from django.template import loader
from .models import Player
from player_info.api.make_requests import Api_Request

def player_info(request):
    myplayers = Player.objects.all().values()
    template = loader.get_template('all_players.html')
    context = {
        'myplayers': myplayers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    playerapi = Api_Request()
    myplayer = Player.objects.get(id=id)
    playerapi.set_player_tag(myplayer.player_id)
    template = loader.get_template('details.html')
    context = {
        'myplayer': myplayer,
        'playerapi': playerapi,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def top_global(request):
    rankingsapi = Api_Request()
    topglobalplayerstags = rankingsapi.get_leaderboard_player_tags()
    template = loader.get_template('top_global.html')
    context = {
        'topglobalplayerstags': topglobalplayerstags,
    }
    return HttpResponse(template.render(context, request))