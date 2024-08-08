from django.http import HttpResponse
from django.template import loader
from .models import Player

def player_info(request):
    myplayers = Player.objects.all().values()
    template = loader.get_template('all_players.html')
    context = {
        'myplayers': myplayers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myplayer = Player.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myplayer': myplayer,
    }
    return HttpResponse(template.render(context, request))