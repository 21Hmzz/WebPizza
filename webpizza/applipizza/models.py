from django.db import models

# Create your models here.


class Ingredient(models.Model):

    idIngredient = models.AutoField(primary_key=True)

    nomIngredient = models.CharField(
        max_length=50, verbose_name="Le nom de cet l'ingrédient")

    def __str__(self):

        return "ingrédient " + self.nomIngredient


class Pizza(models.Model):

    idPizza = models.AutoField(primary_key=True)

    nomPizza = models.CharField(
        max_length=50, verbose_name="Le nom de cette pizza ")

    prix = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name="Le prix ")
    
    image = models.ImageField( verbose_name="L'image de la pizza",null=True, blank=True)

    promotions = models.BooleanField(
        verbose_name="La pizza est-elle en promotion ?"
    )

    def __str__(self):

        if self.promotions:
            return "Pizza " + self.nomPizza + " : " + str(self.prix/2) + "€ ("+str(self.prix)+"€)"
        else:
            return "Pizza " + self.nomPizza + " : " + str(self.prix) + "€"


class Composition(models.Model):
    class Meta:
        unique_together = ('ingredient', 'pizza')

    idComposition = models.AutoField(primary_key=True)

    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    quantite = models.CharField(max_length=100, verbose_name='la quantité')

    def __str__(self):
        ing = self.ingredient
        piz = self.pizza
        return "ingrédient " + ing.nomIngredient + " fait partie de la pizza " + piz.nomPizza + " (prix = "+str(piz.prix)+"€) (quantité = " + self.quantite+")"


class Avis(models.Model):
    class Meta:
        unique_together = ('pizza', 'commentaire')
    
    idAvis = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, verbose_name="Votre nom")
    note = models.IntegerField(verbose_name="La note", choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(verbose_name="Votre commentaire")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)

    def __str__(self):
        return "Avis sur la pizza " + self.pizza.nomPizza + " : " + self.commentaire + " (note = " + str(self.note) + "/5)"

