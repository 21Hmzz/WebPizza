from django.shortcuts import render

# Create your views here.
from applipizza.models import Pizza, Ingredient, Composition
from applipizza.forms import IngredientForm, PizzaForm, CompositionForm


def pizzas(request):

    lesPizzas = Pizza.objects.all()

    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": lesPizzas},
    )


def pizza(request, pizza_id):

    laPizza = Pizza.objects.get(idPizza=pizza_id)
    compo = Composition.objects.filter(pizza=pizza_id)
    listeIngredients = []
    form = CompositionForm()

    for c in compo:
        ing = Ingredient.objects.get(idIngredient=c.ingredient.idIngredient)
        listeIngredients.append({"nom": ing.nomIngredient, "qte": c.quantite})

    return render(
        request,
        "applipizza/pizza.html",
        {"pizza": laPizza, "compo": listeIngredients, "form": form},
    )


def ingredients(request):

    lesIngredients = Ingredient.objects.all()
    return render(
        request,
        "applipizza/ingredients.html",
        {"ingredients": lesIngredients},
    )


def compositions(request):

    lesCompositions = Composition.objects.all()
    return render(
        request,
        "applipizza/compositions.html",
        {"compositions": lesCompositions},
    )


def formulaireCreationIngredient(request):
    formulaire = IngredientForm()

    return render(
        request,
        "applipizza/formulaireCreationIngredient.html",
        {"form": formulaire},
    )


def creerIngredient(request):
    form = IngredientForm(request.POST)
    if form.is_valid():
        nomIng = form.cleaned_data['nomIngredient']
        ing = Ingredient()
        ing.nomIngredient = nomIng
        ing.save()
        return render(
            request,
            "applipizza/traitementFormulaireCreationIngredient.html",
            {"nom": nomIng},
        )


def formulaireCreationPizza(request):
    formulaire = PizzaForm()

    return render(
        request,
        "applipizza/formulaireCreationPizza.html",
        {"form": formulaire},
    )


def creerPizza(request):
    form = PizzaForm(request.POST)
    if form.is_valid():
        nomPizza = form.cleaned_data['nomPizza']
        prix = form.cleaned_data['prix']
        pizza = Pizza()
        pizza.nomPizza = nomPizza
        pizza.prix = prix
        pizza.save()
        return render(
            request,
            "applipizza/traitementFormulaireCreationPizza.html",
            {"nom": nomPizza, "prix": prix},
        )
