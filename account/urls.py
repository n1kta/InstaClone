from django.urls import path
from django.contrib.auth import views as auth_view

from .views import *

urlpatterns = [
    path('', login_required(DashboardListView.as_view()), name='dashboard'),

    path('post/create/', login_required(UserCreatePost.as_view()), name='create_post'),
    path('post/<slug:slug>/', login_required(DashboardDetailView.as_view()), name='dashboard_detail'),

    path('review/<int:pk>/', login_required(AddReview.as_view()), name='review_add'),

    path('account/login/', auth_view.LoginView.as_view(), name='login'),
    path('account/logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('account/registration/', register, name='register'),
    path('account/password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('account/password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('account/reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('users/follow/', login_required(UserFollowView.as_view()), name='user_follow'),
    path('users/like/', login_required(UserLikeView.as_view()), name='users_like'),
    path('users/search/', login_required(UserSearchView.as_view()), name='user_search'),
    path('users/edit/<slug:slug>/', login_required(UserEditView.as_view()), name='user_edit'),
    path('<slug:slug>/', login_required(UserDetailView.as_view()), name='user_detail'),
]