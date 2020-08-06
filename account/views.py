from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse

from images.models import Image, Review
from images.forms import ReviewForm
from .models import *
from .forms import *


class DashboardListView(ListView):
    template_name = 'account/dashboard.html'
    context_object_name = 'images'

    def get_queryset(self):
        contact = Contact.objects.filter(user_from=self.request.user).values('user_to')
        images = Image.objects.filter(user__in=contact)
        return images


class DashboardDetailView(DetailView):
    model = Image
    template_name = 'account/dashboard_detail.html'
    context_object_name = 'image'


class AddReview(View):
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


class UserLikeView(View):
    def post(self, request):
        user_id = request.POST.get('user')
        image_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and image_id and action:
            try:
                user = User.objects.get(id=user_id)
                if action == 'like':
                    Image.objects.get(id=image_id).users_like.add(user)
                else:
                    Image.objects.get(id=image_id).users_like.remove(user)
                return JsonResponse({'status': 'ok'})
            except:
                print('except')
                return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'ok'})


class UserDetailView(DetailView):
    model = User
    template_name = 'account/account/detail.html'
    slug_field = 'username'
    context_object_name = 'current_user'


class UserFollowView(View):
    def post(self, request):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                if action == 'follow':
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'ok'})


class UserCreatePost(View):
    def post(self, request):
        return render(request, 'account/account/create_post.html')

    def get(self, request):
        form = PostForm()
        return render(request, 'account/account/create_post.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password2'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/registration.html', {'form': form})
