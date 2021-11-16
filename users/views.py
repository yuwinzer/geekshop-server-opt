from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from users.models import User


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
        else: print(form.errors)
    else:
        form = UserLoginForm()


    context = {'title': 'Geekshop - Авторизация',
               'form': form
               }
    return render(request, 'users/login.html', context)

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            # form.save()
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, 'Автоматическое письмо отправлено, '
                                          'перейдите по ссылке из письма')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.error(request, 'Автоматическое письмо не отправлено')
                return HttpResponseRedirect(reverse('users:login'))
    else:
        form = UserRegistrationForm()
    context = {'title': 'GeekShop - Регистрация', 'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    user = request.user
    # from users.models import User
    # user = User.objects.get(id=request.user.id)  # если не из реквеста, а обращаться к БД
    if request.method == 'POST':
        form = UserProfileForm(instance=user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=user)

    context = {
        'title' : 'GeekShop - Профиль',
        'form' : form,
        'baskets' : Basket.objects.filter(user=user),
    }
    return render (request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

def send_verify_mail(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} ' \
              f'на портале {settings.DOMAIN_NAME} перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message,settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'users/verification.html')
    except Exception as e:
        print(f'error activation user: {e.args}')
        return HttpResponseRedirect(reverse('main'))

