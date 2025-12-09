from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import *


class GameListView(ListView):
    """Display all GameTitle objects."""
    
    model = GameTitle
    template_name = "project/game_list.html"
    context_object_name = "games"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q))
        return qs


class GameDetailView(DetailView):
    """Display a single GameTitle."""

    model = GameTitle
    template_name = "project/game_detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.object
        q = self.request.GET.get("q")
        matches = game.matches.all().order_by("-match_date")
        if q:
            matches = matches.filter(
                Q(tournament_name__icontains=q) |
                Q(team_one_name__icontains=q) |
                Q(team_two_name__icontains=q) |
                Q(status__icontains=q)
            )

        context["matches"] = matches
        context["query"] = q
        return context


class PlayerListView(ListView):
    """Display all ProPlayers."""

    model = ProPlayer
    template_name = "project/player_list.html"
    context_object_name = "players"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(ign__icontains=q) |
                Q(real_name__icontains=q) |
                Q(team_name__icontains=q) |
                Q(region__icontains=q) |
                Q(game__name__icontains=q)
            )
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            favorite_ids = set(
                FavoritePlayer.objects
                .filter(user=user)
                .values_list("player_id", flat=True)
            )
        else:
            favorite_ids = set()

        context["favorite_ids"] = favorite_ids
        return context


class PlayerDetailView(DetailView):
    """Display a single ProPlayer."""

    model = ProPlayer
    template_name = "project/player_detail.html"
    context_object_name = "player"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context["favorite_ids"] = set(
                FavoritePlayer.objects
                .filter(user=user)
                .values_list("player_id", flat=True)
            )
        else:
            context["favorite_ids"] = set()
            
        q = self.request.GET.get("q")
        stats = self.object.match_stats.all()

        if q:
            stats = stats.filter(
                Q(match__tournament_name__icontains=q) |
                Q(map_name__icontains=q) |
                Q(match__match_date__icontains=q)
            )

        context["filtered_stats"] = stats
        return context


class MatchListView(ListView):
    """Display all matches."""

    model = Match
    template_name = "project/match_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get("q")

        base_qs = Match.objects.all()

        if q:
            base_qs = base_qs.filter(
                Q(tournament_name__icontains=q) |
                Q(team_one_name__icontains=q) |
                Q(team_two_name__icontains=q) |
                Q(game__name__icontains=q)
            )

        context["upcoming_matches"] = base_qs.filter(status=Match.STATUS_UPCOMING).order_by("match_date")
        context["live_matches"] = base_qs.filter(status=Match.STATUS_LIVE).order_by("match_date")
        context["finished_matches"] = base_qs.filter(status=Match.STATUS_FINISHED).order_by("-match_date")

        return context


class MatchDetailView(DetailView):
    """Display a single Match."""

    model = Match
    template_name = "project/match_detail.html"
    context_object_name = "match"


class PlayerMatchStatsDetailView(DetailView):
    """Display stats for a single PlayerMatchStats record."""

    model = PlayerMatchStats
    template_name = "project/stats_detail.html"
    context_object_name = "stats"

class HomeView(TemplateView):
    template_name = "project/home.html"

class FantasyHomeView(TemplateView):
    template_name = "project/fantasy_home.html"

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''

    template_name = 'project/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The url to redirect to after creating a new User.'''
        return reverse('login')
    
class WatchlistView(LoginRequiredMixin, ListView):
    """Show only the players that the current user has favorited."""
    model = ProPlayer
    template_name = "project/watchlist.html"
    context_object_name = "players"

    def get_queryset(self):
        qs = (
            ProPlayer.objects
            .filter(favorited_by__user=self.request.user)
            .select_related("game")
        )

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(ign__icontains=q) |
                Q(team_name__icontains=q) |
                Q(game__name__icontains=q)
            )

        return qs
    
class AddFavoriteView(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        player_pk = kwargs.get("pk")
        player = ProPlayer.objects.filter(pk=player_pk).first()

        if player:
            FavoritePlayer.objects.get_or_create(user=request.user, player=player)

        # go back to where we came from, or fallback to player detail
        next_url = request.META.get("HTTP_REFERER") or reverse("player_detail", args=[player_pk])
        return HttpResponseRedirect(next_url)

        
class RemoveFavoriteView(LoginRequiredMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        player_pk = kwargs.get("pk")
        player = ProPlayer.objects.filter(pk=player_pk).first()

        if player:
            FavoritePlayer.objects.filter(user=request.user, player=player).delete()

        next_url = request.META.get("HTTP_REFERER") or reverse("player_detail", args=[player_pk])
        return HttpResponseRedirect(next_url)
