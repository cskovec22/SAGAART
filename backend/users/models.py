from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from art_gallery.models import Category, Style


MAX_LEN_OTP = 4
MAX_LEN_FIO = 150
MAX_LEN_EMAIL = 254
MAX_LEN_USER_RIGHTS = 50


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    USER = "user"
    MODERATOR = "moderator"
    SEPERUSER = "superuser"
    USER_RIGHTS_CHOICES = [
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (SEPERUSER, "Администратор"),
    ]

    phone = PhoneNumberField()
    email = models.EmailField(
        "Адрес электронной почты",
        max_length=MAX_LEN_EMAIL,
        unique=True,
        validators=[EmailValidator],
    )
    first_name = models.CharField(
        "Имя",
        max_length=MAX_LEN_FIO
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=MAX_LEN_FIO
    )
    surname = models.CharField(
        "Отчество",
        max_length=MAX_LEN_FIO
    )
    favorite_style = models.ManyToManyField(
        Style,
        related_name="users_like",
        verbose_name="Любимые стили"
    )
    favorite_category = models.ManyToManyField(
        Category,
        related_name="users_like",
        verbose_name="Любимые категории"
    )
    # favorite_artist = models.CharField()
    # subscription = models.ForeignKey()
    user_rights = models.CharField(
        "Права пользователя",
        max_length=MAX_LEN_USER_RIGHTS,
        choices=USER_RIGHTS_CHOICES
    )
    create_at = models.DateTimeField(
        "Дата cоздания",
        auto_now_add=True
    )
    otc = models.CharField(
        "Одноразовый код",
        max_length=MAX_LEN_OTP
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        """Конфигурация кастомной модели пользователя."""
        ordering = ("id",)
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"
        constraints = [
            models.UniqueConstraint(
                fields=("phone", "email"),
                name="unique_phone_email"
            )
        ]

    def __str__(self):
        """Строковое представление объекта пользователя."""
        return self.get_full_name()
