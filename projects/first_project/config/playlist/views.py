from django.shortcuts import render

from playlist.models import Video


def playlist(request):
    videos = Video.objects.all()
    return render(request, 'playlist/playlist.html', {'videos': videos})