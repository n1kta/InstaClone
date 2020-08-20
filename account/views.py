from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.mail import send_mail

from images.models import Image, Review
from images.forms import *
from actions.utils import *
from .models import *
from .forms import *

import redis


r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)


# DASHBOARD

class DashboardListView(ListView):
    """Главная Страница"""
    template_name = 'account/dashboard.html'
    context_object_name = 'images'
    paginate_by = 3

    def get_queryset(self):
        contact = Contact.objects.filter(user_from=self.request.user).values('user_to')
        images = Image.objects.filter(user__in=contact)
        return images


# class DashboardDetailView(DetailView):
#     """Подробнее о посте"""
#     model = Image
#     template_name = 'account/dashboard_detail.html'
#     context_object_name = 'image'


class DashboardDetailView(View):
    def get(self, request, slug):
        image = get_object_or_404(Image, slug=slug)
        total_views = r.incr(f'image:{image.id}:views')
        r.zincrby('ranking_for_image', 1, image.id)
        return render(request, 'account/dashboard_detail.html', {'image': image, 'total_views': total_views})


class DashboardRankingView(View):
    """Самые популярные посты(по просмотрам)"""
    def get(self, request):
        image_ranking = r.zrange('ranking_for_image', 0, -1, desc=True)[:10]
        image_ranking_ids = [int(id) for id in image_ranking]
        most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
        most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
        return render(request, 'account/explore.html', {'most_viewed': most_viewed})


# POST

class PostEditView(View):
    def get(self, request, pk):
        post = Image.objects.get(id=pk)
        form = PostForm(instance=post)
        return render(request, 'post/edit_post.html', {'form': form})

    def post(self, request, pk):
        post = Image.objects.get(id=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


class PostDeleteView(View):
    def get(self, request, pk):
        return render(request, 'post/delete_post.html')

    def post(self, request, pk):
        post = Image.objects.get(id=pk)
        post.delete()
        return redirect('dashboard')


# FEEDS

class FeedsView(View):
    def get(self, request):
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id', flat=True)
        if following_ids:
            actions = Action.objects.filter(user_id__in=following_ids)
        actions = actions[:10]
        return render(request, 'account/feeds.html', {'actions': actions})


# USER

def register(request):
    """Регестрация"""
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


class UserFollowView(View):
    """Система подписок"""
    def post(self, request):
        user_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and action:
            try:
                user = User.objects.get(id=user_id)
                if action == 'follow':
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'ok'})
            except User.DoesNotExist:
                return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'ok'})


class UserLikeView(View):
    """Система лайков"""
    def post(self, request):
        user_id = request.POST.get('user')
        image_id = request.POST.get('id')
        action = request.POST.get('action')
        if user_id and image_id and action:
            try:
                user = User.objects.get(id=user_id)
                image = Image.objects.get(id=image_id)
                if action == 'like':
                    image.users_like.add(user)
                    create_action(request.user, 'likes', image)
                else:
                    image.users_like.remove(user)
                return JsonResponse({'status': 'ok'})
            except:
                print('except')
                return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'ok'})


class UserDetailView(DetailView):
    """Информация о пользователе"""
    model = User
    template_name = 'account/account/detail.html'
    slug_field = 'username'
    context_object_name = 'current_user'


class UserCreatePost(View):
    """Создание нового поста"""
    def post(self, request):
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.profile = Profile.objects.get(user=request.user)
            new_post.save()
            return redirect('dashboard')

    def get(self, request):
        form = PostForm()
        return render(request, 'account/account/create_post.html', {'form': form})


class UserEditView(View):
    """Изменение поста"""
    def post(self, request, slug):
        user = User.objects.get(username=slug)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    def get(self, request, slug):
        user = User.objects.get(username=slug)
        form = UserEditForm(instance=user)
        return render(request, 'account/account/change_settings.html', {'form': form})


class UserSearchView(View):
    """Поис по юзеру"""
    def post(self, request):
        url_search = request.POST.get('search')
        if url_search:
            users = User.objects.filter(username__icontains=url_search)
        else:
            users = User.objects.all()
        return render(request, 'account/account/user_search.html', {'users': users})

    def get(self, request):
        return render(request, 'account/account/user_search.html')