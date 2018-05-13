from django.contrib.auth.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from .models import Board, Move


class BoardTestCase(TestCase):
    """This class defines the test suite for the board model."""

    def setUp(self):
        self.user = self.setup_user()
        self.board = Board(created_by=self.user)

    def setup_user(self):
        User = get_user_model()

        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_model_can_create_a_board(self):
        old_count = Board.objects.count()
        self.board.save()
        new_count = Board.objects.count()
        self.assertNotEqual(old_count, new_count)


class MoveTestCase(TestCase):
    """This class defines the test suite for the move model."""

    def setUp(self):
        self.board = Board()

    def test_model_can_create_a_move(self):
        old_count = Move.objects.filter(pk=self.board.pk)
        self.move = Move(board_id=self.board.pk, to_position='e2e4')
        new_count = Move.objects.filter(pk=self.board.pk)
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test suite for the Board views."""

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'test')

    def test_call_view_loads(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chess_game.html')


class APITestCase(TestCase):
    """Test suite for the API views."""

    def setUp(self):
        self.client = APIClient()

        self.user = self.setup_user()
        self.user.save()

        self.client.force_authenticate(self.user)

        self.board = Board(created_by=self.user)
        self.board.save()

    def setup_user(self):
        User = get_user_model()

        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_api_can_create_a_new_board(self):
        response = self.client.post(
            '/api/v1/boards/',
            {
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "created_by": self.user.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], self.board.pk + 1)

    def test_api_can_get_list_of_boards(self):
        response = self.client.get('/api/v1/boards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_get_detail_of_board(self):
        response = self.client.get('/api/v1/boards/{}/'.format(self.board.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_board_detail_is_correct(self):
        response = self.client.get('/api/v1/boards/{}/'.format(self.board.pk))
        self.assertEqual(response.data['id'], self.board.pk)
        self.assertEqual(response.data['fen'], self.board.fen)

        date_started_str = self.board.date_started.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertEqual(response.data['date_started'], date_started_str)
        self.assertEqual(response.data['date_ended'], self.board.date_ended)
        self.assertEqual(response.data['is_won'], self.board.is_won)

    def test_api_can_post_valid_move(self):
        response = self.client.post(
            '/api/v1/boards/{}/moves/'.format(self.board.pk),
            {
                "to_position": "e2e4"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_get_recognizes_move(self):
        post_response = self.client.post(
            '/api/v1/boards/{}/moves/'.format(self.board.pk),
            {
                "to_position": "e2e4"
            }
        )
        get_response = self.client.get('/api/v1/boards/{}/'.format(self.board.pk))
        self.assertEqual(
            get_response.data['fen'],
            'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
        )

    def test_api_can_deny_invalid_move(self):
        response = self.client.post(
            '/api/v1/boards/{}/moves/'.format(self.board.pk),
            {
                "to_position": "e2e6"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_responds_to_winning_move(self):
        moves = ['e2e4', 'b8c6', 'g1e2', 'c6e5', 'c2c3']

        for move in moves:
            response = self.client.post(
                '/api/v1/boards/{}/moves/'.format(self.board.pk),
                {
                    "to_position": move
                }
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        finisher = self.client.post(
            '/api/v1/boards/{}/moves/'.format(self.board.pk),
            {
                "to_position": 'e5d3'
            }
        )
        self.assertTrue(finisher.data['is_won'])

    def test_api_get_latest_board(self):
        latest_board = Board.objects.latest(field_name='date_started')
        get_response = self.client.get('/api/v1/boards/?top=1'.format(self.board.pk))
        self.assertEqual(latest_board.id, get_response.data[0]['id'])
