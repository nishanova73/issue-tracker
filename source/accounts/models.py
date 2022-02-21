from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name="profile",
        verbose_name="Profile",
        on_delete=models.CASCADE,
    )

    birth_date = models.DateField(
        null=True,
        blank=False,
        verbose_name="Date of birth",
    )

    avatar = models.ImageField(
        verbose_name="Avatar",
        upload_to="avatars/",
        null=True,
        blank=False
    )

    link = models.URLField(
        max_length=200,
        null=True,
        blank=False
    )

    about_field = models.TextField(
        max_length=200,
        null=True,
        blank=False,
        verbose_name="About"
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"Profile: {self.user.username}. {self.id}"