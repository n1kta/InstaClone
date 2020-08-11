from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import *
from .forms import ReviewForm


# COMMENTS

class AddReview(View):
    """Добавить комментарий"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        post = Image.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.user = request.user
            form.post = post
            form.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
