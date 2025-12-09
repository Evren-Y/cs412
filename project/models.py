from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class GameTitle(models.Model):
    '''Model for each esports game being tracked (e.g., Valorant, CS2).'''

    name = models.TextField(blank=True)
    region = models.TextField(default="Global")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"


class ProPlayer(models.Model):
    '''Professional player instance tied to a game.'''

    ign = models.TextField(blank=True)
    real_name = models.TextField(blank=True)
    region = models.TextField(blank=True)
    team_name = models.TextField(blank=True)
    game = models.ForeignKey(GameTitle, on_delete=models.CASCADE, related_name="players")
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f"{self.ign} ({self.game.name})"


class Match(models.Model):
    '''Scheduled or completed matches for a game.'''

    STATUS_UPCOMING = "upcoming"
    STATUS_LIVE = "live"
    STATUS_FINISHED = "finished"
    STATUS_CHOICES = [
        (STATUS_UPCOMING, "Upcoming"),
        (STATUS_LIVE, "Live"),
        (STATUS_FINISHED, "Finished"),
    ]

    game = models.ForeignKey(GameTitle, on_delete=models.CASCADE, related_name="matches")
    tournament_name = models.TextField(blank=True)
    match_date = models.DateTimeField()
    team_one_name = models.TextField(blank=True)
    team_two_name = models.TextField(blank=True)
    best_of = models.PositiveSmallIntegerField(default=3)
    status = models.TextField(choices=STATUS_CHOICES, default=STATUS_UPCOMING)
    team_one_score = models.PositiveSmallIntegerField(default=0)
    team_two_score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.tournament_name}: {self.team_one_name} vs {self.team_two_name}"


class PlayerMatchStats(models.Model):
    '''Performance stats of a single player.'''

    player = models.ForeignKey(ProPlayer, on_delete=models.CASCADE, related_name="match_stats")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="player_stats")
    map_name = models.TextField(blank=True)
    kills = models.PositiveSmallIntegerField()
    deaths = models.PositiveSmallIntegerField()
    assists = models.PositiveSmallIntegerField()
    acs = models.FloatField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ("player", "match", "map_name")

    def __str__(self):
        return f"{self.player.ign} – {self.map_name} – {self.match}"
    

class FavoritePlayer(models.Model):
    '''An instance of an authenticated user's saved favorited players.'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_players"
    )
    player = models.ForeignKey(
        ProPlayer,
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "player")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.player.ign}"