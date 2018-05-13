import chess

from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Board, Move
from .serializers import BoardSerializer, MoveSerializer, UserSerializer


class BoardList(generics.ListCreateAPIView):
    # TODO - remove these?
    authentication_classes = ()
    permission_classes = ()

    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        queryset = Board.objects.order_by('-date_started')
        top_count = self.request.query_params.get('top', None)
        if top_count is not None:
            queryset = queryset[:int(top_count)]
        return queryset


class BoardDetail(generics.RetrieveAPIView):
    # TODO - remove these?
    authentication_classes = ()
    permission_classes = ()

    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class MoveList(generics.ListCreateAPIView):

    @staticmethod
    def validate_move(data):
        board_pk = data.get('board')
        to_position = data.get('to_position')
        data['response'] = status.HTTP_201_CREATED

        # Get the request board Model instance
        board = Board.objects.get(pk=board_pk)

        # Check that the game has not ended
        if not board.date_ended:

            # Initialize validator with board FEN
            chess_validator = chess.Board(board.fen)

            # Check and make the move
            chess_move = chess.Move.from_uci(to_position)
            if chess_move in chess_validator.legal_moves:
                chess_validator.push(chess_move)

                # Check if the game is over
                if chess_validator.is_game_over(claim_draw=False):
                    board.date_ended = timezone.now()
                    if chess_validator.result() == '0-1':
                        board.is_won = True
                    elif chess_validator.result() == '1-0':
                        board.is_won = False
                    elif chess_validator.result() == '1/2-1/2':
                        board.is_won = False  # TODO// Add a draw flag
                    else:
                        data['error'] = "Invalid Game Result"
                        data['response'] = status.HTTP_500_INTERNAL_SERVER_ERROR
                        return False, data

                # Make modification and save the board
                board.fen = chess_validator.fen()
                board.save()
                data['is_won'] = board.is_won
                return True, data
            else:
                data['error'] = "Invalid: {}.".format(chess_move)
                data['response'] = status.HTTP_400_BAD_REQUEST
                return False, data
        else:
            data['error'] = "Game has already ended."
            data['response'] = status.HTTP_400_BAD_REQUEST
            return False, data

    def post(self, request, *args, **kwargs):
        board = Board.objects.get(pk=kwargs['pk'])

        if not request.user == board.created_by:
            raise PermissionDenied("You can not move on this board.")

        post_data = {
            'board': board.pk,
            'to_position': request.data.get('to_position'),
        }
        serializer = MoveSerializer(data=post_data)

        if serializer.is_valid():

            move_is_valid, move_data = self.validate_move(data=post_data)

            if move_is_valid:
                serializer.save()
                return Response(move_data, status.HTTP_201_CREATED)
                # return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Move.objects.filter(board_id=self.kwargs['pk'])
        return queryset

    serializer_class = MoveSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
