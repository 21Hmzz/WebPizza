from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg

# Create your views here.
from applipizza.models import Pizza, Ingredient, Composition, Avis
from applipizza.forms import IngredientForm, PizzaForm, CompositionForm, AvisForm



def pizzas(request):
    lesPizzas = Pizza.objects.all()
    nbPizzas = Pizza.objects.count()
    AvisFormv = AvisForm()
    page = request.GET.get('page')
    for p in lesPizzas:
        moyennePizza = Avis.objects.filter(pizza=p.idPizza).aggregate(Avg('note'))
        if moyennePizza['note__avg'] is not None:
            p.moyenne = moyennePizza['note__avg']
        else:
            p.moyenne = "Pas encore d'avis"

    paginator = Paginator(lesPizzas, 3)
    try:
        lesPizzas = paginator.page(page)
    except PageNotAnInteger:
        lesPizzas = paginator.page(1)
    except EmptyPage:
        lesPizzas = paginator.page(paginator.num_pages)
    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": lesPizzas, "nbPizzas": nbPizzas, "AvisForm": AvisFormv},
    )


def pizza(request, pizza_id):

    laPizza = Pizza.objects.get(idPizza=pizza_id)
    compo = Composition.objects.filter(pizza=pizza_id)
    listeIngredients = []
    form = CompositionForm()
    avis = Avis.objects.filter(pizza=pizza_id)

    for c in compo:
        ing = Ingredient.objects.get(idIngredient=c.ingredient.idIngredient)
        listeIngredients.append(
            {"nom": ing.nomIngredient, "qte": c.quantite, "idComposition": c.idComposition})

    return render(
        request,
        "applipizza/pizza.html",
        {"pizza": laPizza, "compo": listeIngredients, "form": form, "avis": avis},
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
    nbPizzas = Pizza.objects.count()
    AvisFormv = AvisForm()
    page = request.GET.get('page')
    for p in lesPizzas:
        moyennePizza = Avis.objects.filter(pizza=p.idPizza).aggregate(Avg('note'))
        if moyennePizza['note__avg'] is not None:
            p.moyenne = moyennePizza['note__avg']
        else:
            p.moyenne = "Pas encore d'avis"

    paginator = Paginator(lesPizzas, 3)
    try:
        lesPizzas = paginator.page(page)
    except PageNotAnInteger:
        lesPizzas = paginator.page(1)
    except EmptyPage:
        lesPizzas = paginator.page(paginator.num_pages)
    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": lesPizzas, "nbPizzas": nbPizzas, "AvisForm": AvisFormv},
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
    form = PizzaForm(request.POST, request.FILES)
    if form.is_valid():
        nomPizza = form.cleaned_data['nomPizza']
        prix = form.cleaned_data['prix']
        promotions = form.cleaned_data['promotions']
        pizza = Pizza.objects.get(idPizza=pizza_id)
        pizza.nomPizza = nomPizza
        pizza.prix = prix
        pizza.promotions = promotions

        if request.FILES:
            image = request.FILES['image']
            pizza.image = image
        else : 
            pizza.image = pizza.image

        pizza.save()
        return render(
            request,
            "applipizza/traitementFormulaireModificationPizza.html",
            {"nom": nomPizza, "prix": prix},
        )
    else :
        print(form._errors)
        pizza = Pizza.objects.get(idPizza=pizza_id)
        return render(
            request,
            "applipizza/formulaireModificationPizza.html",
            {"pizza": pizza, "form": form, "errors": form._errors},
        )



def formulaireCreationPizza(request):
    formulaire = PizzaForm()

    return render(
        request,
        "applipizza/formulaireCreationPizza.html",
        {"form": formulaire},
    )

def avis(request):
    form = AvisForm(request.POST)
    if form.is_valid():
        nom = form.cleaned_data['nom']
        avis = form.cleaned_data['commentaire']
        note = form.cleaned_data['note']
        pizza = form.cleaned_data['pizza']

        a = Avis()
        a.nom = nom
        a.commentaire = avis
        a.note = note
        a.pizza = pizza
        a.save()


    lesPizzas = Pizza.objects.all()
    nbPizzas = Pizza.objects.count()
    AvisFormv = AvisForm()
    page = request.GET.get('page')
    for p in lesPizzas:
        moyennePizza = Avis.objects.filter(pizza=p.idPizza).aggregate(Avg('note'))
        if moyennePizza['note__avg'] is not None:
            p.moyenne = moyennePizza['note__avg']
        else:
            p.moyenne = "Pas encore d'avis"
    paginator = Paginator(lesPizzas, 3)
    try:
        lesPizzas = paginator.page(page)
    except PageNotAnInteger:
        lesPizzas = paginator.page(1)
    except EmptyPage:
        lesPizzas = paginator.page(paginator.num_pages)
    return render(
        request,
        "applipizza/pizzas.html",
        {"pizzas": lesPizzas, "nbPizzas": nbPizzas, "AvisForm": AvisFormv},
    )


def creerPizza(request):
    form = PizzaForm(request.POST, request.FILES)
    if form.is_valid():
        nomPizza = form.cleaned_data['nomPizza']
        prix = form.cleaned_data['prix']
        image = request.FILES['image']
        promotions = form.cleaned_data['promotions']
        
        pizza = Pizza()
        pizza.nomPizza = nomPizza
        pizza.prix = prix
        pizza.image = image
        pizza.promotions = promotions
        
        pizza.save()
        return render(
            request,
            "applipizza/traitementFormulaireCreationPizza.html",
            {"nom": nomPizza, "prix": prix, "image": image},
        )
    print(form._errors)
    
 


def ingredients(request):

    lesIngredients = Ingredient.objects.all()
    nbIngredients = Ingredient.objects.count()
    page = request.GET.get('page')
    paginator = Paginator(lesIngredients, 10)
    try:
        lesIngredients = paginator.page(page)
    except PageNotAnInteger:
        lesIngredients = paginator.page(1)
    except EmptyPage:
        lesIngredients = paginator.page(paginator.num_pages)

    return render(
        request,
        "applipizza/ingredients.html",
        {"ingredients": lesIngredients, "nbIngredients": nbIngredients},
    )


def compositions(request):

    lesCompositions = Composition.objects.all()
    nbCompositions = Composition.objects.count()
    page = request.GET.get('page')
    paginator = Paginator(lesCompositions, 10)
    try:
        lesCompositions = paginator.page(page)
    except PageNotAnInteger:
        lesCompositions = paginator.page(1)
    except EmptyPage:
        lesCompositions = paginator.page(paginator.num_pages)

    return render(
        request,
        "applipizza/compositions.html",
        {"compositions": lesCompositions, "nbCompositions": nbCompositions},
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

