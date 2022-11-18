from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("api/create/<name>", views.create, name="create"),
    path("api/scanned/<code>", views.scanned, name="scanned"),
    path("stats/<code>", views.stats, name="stats"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("api/start", views.start, name="start"),
    path("api/test", views.test, name="test"),
    path("loaderio", views.loaderio, name="loaderio")
]
