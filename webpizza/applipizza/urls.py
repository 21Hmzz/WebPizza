
from django.urls import path
from applipizza import views

urlpatterns = [
    path('', views.pizzas),
    path('pizzas/', views.pizzas),
    path('pizzas/<int:pizza_id>', views.pizza),
    path('pizzas/<int:pizza_id>/update',
         views.afficherFormulaireModificationPizza),
    path('pizzas/<int:pizza_id>/updated',
         views.modifierPizza),
    path('pizzas/<int:pizza_id>/delete', views.supprimerPizza),
    path('pizzas/add', views.formulaireCreationPizza),
    path('pizzas/<int:pizza_id>/addIngredient',
         views.ajouterIngredientDansPizza),
    path('pizzas/<int:pizza_id>/deleteIngredient/<int:composition_id>',
         views.supprimerIngredientDansPizzaPizza),
    path('pizzas/create', views.creerPizza),
    path('ingredients/', views.ingredients),
    path('ingredients/add', views.formulaireCreationIngredient),
    path('ingredients/create', views.creerIngredient),

    path('compositions/', views.compositions)
]
