from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *

app_name = 'images'

urlpatterns = [
    path('review/<int:pk>/', login_required(AddReview.as_view()), name='review_add'),
]