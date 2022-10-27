from django.urls import path

# from recipes.views import home
from . import views

# from recipes.views import contato, principal, sobre
# estamos importando as funções do arquivo views, da pasta recipes

app_name = 'recipes'

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    # <int:id> é o parâmetro (com o seu tipo int)
    # que será repassado para views.recipe
    # outros tipos: str (qualquer string),
    # slug (alfanumérico com - ou _) e uuid
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipe_api_v1"
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailApi.as_view(),
        name="recipe_api_v1_detail"
    ),
]
