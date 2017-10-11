from django.db import models


class Card(models.Model):

    number = models.CharField(
        verbose_name='Number',
        unique=True,
        max_length=16
    )

    year = models.PositiveSmallIntegerField(
        verbose_name='Year'
    )

    month = models.PositiveSmallIntegerField(
        verbose_name='Month'
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=50
    )
