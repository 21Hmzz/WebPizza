from django import forms
from django.forms import ModelForm
from applipizza.models import Pizza, Ingredient, Composition, Avis


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['nomIngredient']


class PizzaForm(ModelForm):
    class Meta:
        model = Pizza
        image = forms.ImageField()
        promotions = forms.BooleanField()
        fields = ['nomPizza', 'prix', 'image', 'promotions']


class CompositionForm(ModelForm):
    class Meta:
        model = Composition
        fields = ['ingredient', 'quantite']

class AvisForm(ModelForm):
    class Meta:
        model = Avis
       
        fields = ['nom','commentaire', 'note', 'pizza']