from django.db import models

class Player(models.Model):
    player_id = models.CharField(max_length=10)
    player_name = models.CharField(max_length=255)
