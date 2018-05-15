from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Board


@login_required
def board_game_view(request):
    # TODO - have to make sure that the JS consumer performs the same!!
    board = Board.objects.filter(created_by=request.user).latest('date_started')
    return render(request, 'chess_game.html', {'user': request.user, 'board': board})


def test_game_view(request):
    return render(request, 'test_game.html', {})
