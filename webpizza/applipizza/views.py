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
        listeIngredients.append(
            {"nom": ing.nomIngredient, "qte": c.quantite, "idComposition": c.idComposition})

    return render(
        request,
        "applipizza/pizza.html",
        {"pizza": laPizza, "compo": listeIngredients, "form": form},
    )


def ajouterIngredientDansPizza(request, pizza_id):
    form = CompositionForm(request.POST)
    compos = Composition.objects.filter(pizza=pizza_id)
    if form.is_valid():

        ing = form.cleaned_data['ingredient']
        qte = form.cleaned_data['quantite']
        if compos.filter(ingredient=ing).exists():
            compo = compos.get(ingredient=ing)
            compo.delete()

        compo = Composition()
        compo.pizza = Pizza.objects.get(idPizza=pizza_id)
        compo.ingredient = Ingredient.objects.get(
            idIngredient=ing.idIngredient)
        compo.quantite = qte
        compo.save()

        # regeneration de la vue pizza

        laPizza = Pizza.objects.get(idPizza=pizza_id)
        form = CompositionForm()
        compo = Composition.objects.filter(pizza=pizza_id)
        listeIngredients = []
        for c in compo:
            ing = Ingredient.objects.get(
                idIngredient=c.ingredient.idIngredient)
            listeIngredients.append(
                {"nom": ing.nomIngredient, "qte": c.quantite, "idComposition": c.idComposition})

        return render(
            request,
            "applipizza/pizza.html",
            {"pizza": laPizza, "compo": listeIngredients, "form": form},

        )


def supprimerIngredientDansPizzaPizza(request, pizza_id, composition_id):
    compo = Composition.objects.get(idComposition=composition_id)
    compo.delete()
    pizza = Pizza.objects.get(idPizza=pizza_id)
    compoPizza = Composition.objects.filter(pizza=pizza_id)
    listeIngredients = []
    for c in compoPizza:
        ing = Ingredient.objects.get(idIngredient=c.ingredient.idIngredient)
        listeIngredients.append(
            {"nom": ing.nomIngredient, "qte": c.quantite, "idComposition": c.idComposition})

    form = CompositionForm()
    lesPizzas = Pizza.objects.all()

    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": lesPizzas},
    )


def supprimerPizza(request, pizza_id):
    laPizza = Pizza.objects.get(idPizza=pizza_id)
    laPizza.delete()
    LesPizzas = Pizza.objects.all()
    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": LesPizzas},
    )


def afficherFormulaireModificationPizza(request, pizza_id):
    laPizza = Pizza.objects.get(idPizza=pizza_id)
    form = PizzaForm(instance=laPizza)
    return render(
        request,
        "applipizza/formulaireModificationPizza.html",
        {"pizza": laPizza, "form": form},
    )


def modifierPizza(request, pizza_id):
    form = PizzaForm(request.POST)
    if form.is_valid():
        nomPizza = form.cleaned_data['nomPizza']
        prix = form.cleaned_data['prix']
        pizza = Pizza.objects.get(idPizza=pizza_id)
        pizza.nomPizza = nomPizza
        pizza.prix = prix
        pizza.save()
        return render(
            request,
            "applipizza/traitementFormulaireModificationPizza.html",
            {"nom": nomPizza, "prix": prix},
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
