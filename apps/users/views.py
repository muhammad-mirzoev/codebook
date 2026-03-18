from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser
from .forms import (
    RegisterForm, LoginForm, ProfileEditForm,
    AvatarForm, CoverForm, PrivacyForm
)


# --- Регистрация ---
def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}! 🎉')
            return redirect('home')
        else:
            messages.error(request, 'Проверьте правильность введённых данных.')

    return render(request, 'users/register.html', {'form': form})


# --- Логин ---
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                user.last_seen = timezone.now()
                user.save(update_fields=['last_seen'])
                messages.success(request, f'Привет, {user.username}! 👋')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Неверный email или пароль.')

    return render(request, 'users/login.html', {'form': form})


# --- Логаут ---
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('login')


# --- Профиль (чужой или свой) ---
def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    # если профиль закрытый и смотрит не владелец
    if not profile_user.is_profile_public and request.user != profile_user:
        return render(request, 'users/private_profile.html', {'profile_user': profile_user})

    # книги пользователя (подключим когда будет apps/library)
    context = {
        'profile_user': profile_user,
        'is_owner': request.user == profile_user,
    }
    return render(request, 'users/profile.html', context)


# --- Редактирование профиля ---
@login_required
def profile_edit_view(request):
    form = ProfileEditForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён! ✅')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, 'Ошибка при сохранении.')

    return render(request, 'users/profile_edit.html', {'form': form})


# --- Смена аватара ---
@login_required
def avatar_upload_view(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аватар обновлён! ✅')
        else:
            messages.error(request, 'Ошибка загрузки аватара.')
    return redirect('profile_edit')


# --- Смена баннера ---
@login_required
def cover_upload_view(request):
    if request.method == 'POST':
        form = CoverForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Баннер обновлён! ✅')
        else:
            messages.error(request, 'Ошибка загрузки баннера.')
    return redirect('profile_edit')


# --- Настройки приватности ---
@login_required
def privacy_settings_view(request):
    form = PrivacyForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки сохранены! ✅')
            return redirect('privacy_settings')

    return render(request, 'users/privacy_settings.html', {'form': form})
