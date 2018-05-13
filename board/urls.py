from django.urls import path

# from rest_framework.routers import DefaultRouter

from board.api import views

app_name = 'board'

urlpatterns = [
    # Board
    path('boards/', views.BoardList.as_view(), name='board_list'),
    path('boards/<int:pk>/', views.BoardDetail.as_view(), name='board_detail'),
    path('boards/<int:pk>/moves/', views.MoveList.as_view(), name='move_list'),
    # User
    path('users/', views.UserCreate.as_view(), name='user_create'),
    path('login/', views.LoginView.as_view(), name="login"),
]
