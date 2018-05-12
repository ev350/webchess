from rest_framework import serializers

from ..models import Board, Move


class MoveSerializer(serializers.ModelSerializer):
    """Serializer to map the Move instance to JSON."""

    class Meta:
        model = Move
        # fields = ('id', 'board', 'to_position')
        fields = '__all__'


class BoardSerializer(serializers.ModelSerializer):
    """Serializer to map the Board instance to JSON."""

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('date_started', 'date_ended', 'is_won')
