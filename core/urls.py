from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('movie/<str:pk>/', views.movie, name='movie'),  # динамический url-адресс (pk имя переменной)
    path('my-list', views.my_list, name='my-list'),  # Corrected line with added comma
    path('add-to-list', views.add_to_list, name='add-to-list'),
]