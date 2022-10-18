from django.urls import path

# from recipes.views import home
from . import views

# from recipes.views import contato, principal, sobre
# estamos importando as funções do arquivo views, da pasta recipes

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('register/create/', views.register_create, name="create"),
    path('login/', views.login_view, name="login"),
    path('login/create/', views.login_create, name="login_create"),
    path('logout/', views.logout_view, name="logout"),
]