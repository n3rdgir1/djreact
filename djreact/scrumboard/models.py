from django.core.validators import MinValueValidator
from django.db import models


class List(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"List: {self.name}"


class Card(models.Model):
    """
    A Card
    """
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    list = models.ForeignKey(List, related_name="cards", on_delete=models.CASCADE)
    story_points = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    businessValue = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Card: {self.title}"
