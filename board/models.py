from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Board(models.Model):
    """A chess board."""

    DEFAULT_BOARD = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    PIECE_COLORS = (
        (1, 'w'),
        (2, 'b')
    )

    fen = models.CharField(max_length=256, blank=False, default=DEFAULT_BOARD)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    host_color = models.CharField(max_length=1, blank=False, null=False, choices=PIECE_COLORS)
    date_started = models.DateTimeField(auto_now_add=True)
    date_ended = models.DateTimeField(null=True)
    is_won = models.NullBooleanField()

    def __str__(self):
        return _('Current State: %s') % self.fen


class Move(models.Model):
    """A chess move."""

    board = models.ForeignKey(
        Board, related_name='moves', on_delete=models.CASCADE)
    to_position = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now_add=True)
