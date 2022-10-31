from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("create/<name>", views.create, name="create"),
    path("scanned/<code>", views.scanned, name="scanned"),
    path("stats/<code>", views.stats, name="stats"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("start", views.start, name="start"),
]