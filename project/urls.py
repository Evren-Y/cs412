# file: project/urls.py
# Author: Evren Yaman (yamane@bu.edu), 11/25/2025
# Description: extension of cs412 urls.py file, creating the paths for all pages used in the esports fantasy project web application.

from django.urls import path
from .views import *

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("games/", GameListView.as_view(), name="game_list"),
    path("games/<int:pk>/", GameDetailView.as_view(), name="game_detail"),
    path("players/", PlayerListView.as_view(), name="player_list"),
    path("players/<int:pk>/", PlayerDetailView.as_view(), name="player_detail"),
    path("matches/", MatchListView.as_view(), name="match_list"),
    path("matches/<int:pk>/", MatchDetailView.as_view(), name="match_detail"),
    path("stats/<int:pk>/", PlayerMatchStatsDetailView.as_view(), name="stats_detail"),
    path("watchlist/", WatchlistView.as_view(), name="watchlist"),
    path("players/<int:pk>/favorite/", AddFavoriteView.as_view(), name="add_favorite"),
    path("players/<int:pk>/unfavorite/", RemoveFavoriteView.as_view(), name="remove_favorite"),
    path("fantasy/", FantasyHomeView.as_view(), name="fantasy_home"),

    # user authentication/authorization
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]