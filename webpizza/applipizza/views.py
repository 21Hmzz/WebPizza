from django.shortcuts import render

# Create your views here.
from applipizza.models import Pizza


def pizzas(request):

    lesPizzas = Pizza.objects.all()

    return render(
        request,
        "applipizza/pizzas.html",
        {"Pizzas": lesPizzas},
    )
