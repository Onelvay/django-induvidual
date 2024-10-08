from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Follow
from .forms import ProfileForm
from django.views.decorators.csrf import csrf_exempt

# Регистрация пользователя
@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # Создаем профиль для пользователя
            return redirect('profile', user_id=user.id)  # Перенаправляем на профиль с user_id
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# Просмотр профиля пользователя
def profile_view(request, user_id):  # Добавляем параметр user_id
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'user': user})
# Редактирование профиля
@csrf_exempt
def profile_edit(request):
    user_id = request.GET.get('user_id')
    user = get_object_or_404(User, id=user_id)
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
    else:
        form = ProfileForm(instance=user.profile)

    return render(request, 'users/profile_edit.html', {'form': form})

# Подписка на пользователя
@csrf_exempt
def follow_user(request):
    follower_id = request.GET.get('follower_id')
    following_id = request.GET.get('following_id')
    follower = get_object_or_404(User, id=follower_id)
    following = get_object_or_404(User, id=following_id)
    Follow.objects.create(follower=follower, following=following)
    return redirect('profile', user_id=following.id)

# Отписка от пользователя
@csrf_exempt
def unfollow_user(request):
    follower_id = request.GET.get('follower_id')
    following_id = request.GET.get('following_id')
    follow = get_object_or_404(Follow, follower__id=follower_id, following__id=following_id)
    follow.delete()
    return redirect('profile', user_id=following_id)
