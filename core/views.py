import re
from django.shortcuts import render, redirect
# redirect - служит для перенаправления пользователя
from django.contrib.auth.models import User, auth
# auth - позволяет аутиндифицировать пользователя
from django.contrib import messages
# message - если нужно вывести текст об ошибке
from .models import Movie, MovieList
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Проверка пользователя на регистрацию используя login_required
@login_required(login_url='login')
def index(request):
    movie = Movie.objects.all()

    context = {
        'movies': movie,
    }
    return render(request, 'index.html', context)


@login_required(login_url='login')
def movie(request, pk):
    movie_uuid = pk
    movie_details = Movie.objects.get(uu_id=movie_uuid)

    context = {
        'movie_details': movie_details,
    }

    return render(request, 'movie.html', context)


@login_required(login_url='login')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []

    for movie in movie_list:
        user_movie_list.append(movie.movie)

    context = {
        'movies': user_movie_list
    }
    return render(request, 'my_list.html', context)


@login_required(login_url='login')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None

        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list, created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)

        if created:
            response_data = {'status': 'success', 'message': 'Added'}
        else:
            response_data = {'status': 'info', 'message': 'Movie already this list'}
        
        return JsonResponse(response_data)
    else:
        # return error
        return JsonResponse({'status': 'eror', 'message': 'Invalid request'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверяем, что пользователь равен пользователю и тоже самое с паролем
        user = auth.authenticate(username=username, password=password)
        # Провряем существует ли пользователь
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')


def signup(request):
    # Собираем данные
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Проверяем совподают ли пароли
        if password == password2:
            # Если пароли совподают, делаем следующее:
            # Проверяем почту на то существует ли она
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            # Проверяем пользователя на то существует ли он
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            # Если все отлично и сповподает, сохроняем
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Переводим пользовтеля и делаем аутиндификацию и сохраняем в бд
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')
