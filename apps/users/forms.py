from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


# --- Регистрация ---
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'example@mail.com',
            'class': 'form-input'
        })
    )
    username = forms.CharField(
        label='Имя пользователя',
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ваш никнейм',
            'class': 'form-input'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Минимум 8 символов',
            'class': 'form-input'
        })
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторите пароль',
            'class': 'form-input'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('Этот никнейм уже занят.')
        return username


# --- Логин ---
class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ваш email',
            'class': 'form-input'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ваш пароль',
            'class': 'form-input'
        })
    )


# --- Редактирование основной инфо ---
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'bio',
            'location', 'date_of_birth',
            'vkontact', 'telegram',
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ваш никнейм'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Расскажите о себе...',
                'rows': 4,
                'maxlength': 500
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Город, Страна'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'vkontact': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'vk_username'
            }),
            'telegram': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'telegram_username'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Этот никнейм уже занят.')
        return username


# --- Смена аватара и баннера ---
class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'file-input', 'accept': 'image/*'})
        }


class CoverForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['cover']
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'file-input', 'accept': 'image/*'})
        }


# --- Настройки приватности ---
class PrivacyForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['is_profile_public', 'show_email']
        widgets = {
            'is_profile_public': forms.CheckboxInput(attrs={'class': 'toggle-input'}),
            'show_email': forms.CheckboxInput(attrs={'class': 'toggle-input'}),
        }
        labels = {
            'is_profile_public': 'Публичный профиль',
            'show_email': 'Показывать email в профиле',
        }
