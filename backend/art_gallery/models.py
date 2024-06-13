from django.db import models


LEN_NAME_STYLE = 50
LEN_NAME_CATEGORY = 50


class Style(models.Model):
    """Модель стиля."""
    name = models.CharField("Название", max_length=LEN_NAME_STYLE)


class Category(models.Model):
    """Модель категории."""
    name = models.CharField("Название", max_length=LEN_NAME_CATEGORY)


class Painter(models.Model):
    """Модель художника."""
    pass
