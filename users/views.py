from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserProfileEditForm
from baskets.models import Basket
from users.models import User
from django.db import transaction


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, form.errors)
    else:
        form = UserLoginForm()
    context = {'title': 'GeekShop - Авторизация', 'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_email(user):
                messages.success(request, f'Вам на почту отправлено письмо. '
                                          'Для завершения регистрации перейдите по ссылке в письме')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.error(request, 'Ошибка при отправке письма!' + form.errors)
                return HttpResponseRedirect(reverse('users:registration'))
        messages.error(request, form.errors)
    else:
        form = UserRegistrationForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


@login_required
@transaction.atomic
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        profile_form = UserProfileEditForm(instance=user.userprofile, data=request.POST)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно изменены')
        else:
            if form.is_valid():
                messages.error(request, profile_form.errors)
                print(profile_form.errors)
            else:
                messages.error(request, form.errors)
                print(form.errors)
        return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)
        profile_form = UserProfileEditForm(instance=user.userprofile)

    context = {
        'title': 'GeekShop - Профиль',
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def send_verify_email(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале ' \
              f'{settings.DOMAIN_NAME} перейдите по ссылке {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        exp, mess = user.is_activation_key_expired
        if user.activation_key == activation_key and not exp:
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрированы!')
            return render(request, 'products/index.html')
        else:
            messages.error(request, 'Cсылка для подтверждения регистрации не действительна!\n' +
                           mess)
            return render(request, 'users/verification.html')
    except Exception as e:
        print(f'error user registration: {e.args}')
        return HttpResponseRedirect(reverse('index'))
