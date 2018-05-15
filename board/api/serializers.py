from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import Board, Move, User


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)

        # TODO - create initial board; is here alright?
        init_board = Board(created_by=user)
        init_board.save()

        return user
