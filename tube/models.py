from django.db import models

from panya.models import ModelBase

class AgeRestriction(models.Model):
    """
    Simple age restriction model.
    """
    age = models.IntegerField(
        help_text="Rating age, i.e. 13, 18 etc.",
    )
    symbol = models.CharField(
        max_length=128,
        help_text='Rating symbol, i.e. PG, SN, R, G etc.',
        blank=True,
        null=True,
    )
    description = models.TextField(
        help_text='A short description. Usually an explanation of the symbol, i.e. Parental Guidance Suggested. Some material may not be suitable for children.',
        blank=True,
        null=True,
    )

class Channel(ModelBase):
    """
    Base channel model from which all Channel types should inherit.
    """
    age_restriction = models.ForeignKey(
        'tube.AgeRestriction',
        blank=True,
        null=True,
    )
