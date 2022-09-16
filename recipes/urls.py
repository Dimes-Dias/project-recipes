from django.urls import path

# from recipes.views import home
from . import views

# from recipes.views import contato, principal, sobre
# estamos importando as funções do arquivo views, da pasta recipes

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name="home"),
    # <int:id> é o parâmetro (com o seu tipo int) que será repassado para views.recipe
    # outros tipos: str (qualquer string), slug (alfanumérico com - ou _) e uuid
    path('recipes/category/<int:category_id>/',
         views.category, name="category"),
    path('recipes/<int:id>/', views.recipe, name="recipe"),
]
