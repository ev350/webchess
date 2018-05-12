from django.db import models
from django.utils.translation import ugettext_lazy as _


class Board(models.Model):
    """A chess board."""

    DEFAULT_BOARD = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    fen = models.CharField(max_length=256, blank=False, default=DEFAULT_BOARD)
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
