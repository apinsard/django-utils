# -*- coding: utf-8 -*-
from django.db import models


class Foo(models.Model):

    some_int = models.IntegerField(blank=True, null=True)
    some_string = models.CharField(max_length=254)
    some_text = models.TextField(blank=True)
    some_boolean = models.BooleanField()
    some_nullable_boolean = models.NullBooleanField()
    some_date = models.DateField(null=True)
    some_datetime = models.DateTimeField(null=True)
    some_time = models.TimeField(null=True)


class Bar(models.Model):

    some_foo = models.ForeignKey(Foo, models.CASCADE, null=True)
    some_decimal = models.DecimalField(
        null=True, decimal_places=2, max_digits=6)
    some_float = models.FloatField(null=True)
    some_duration = models.DurationField(null=True)
    some_file = models.FileField(blank=True, null=True)
