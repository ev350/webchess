from django.shortcuts import render


def board_game_view(request):
    return render(request, 'chess_game.html', {})
