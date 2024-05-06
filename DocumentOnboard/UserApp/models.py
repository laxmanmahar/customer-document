from django.db import models
import jsonfield
from UserApp.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import Group

gender = (("M", "male"), ("F", "female"), ("U", "non-binary"))
surname = (("Yes", "yes"), ("No", "no"))

'''Country Model'''


class Country(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self: "Country") -> str:
        return str(self.name)


class DocumentSet(models.Model):
    document_name = models.CharField(max_length=250, null=True, blank=True)
    country = models.ManyToManyField(
        "Country", related_name="relate_country"
    )
    has_backside = models.BooleanField(default=False)
    ocrLable_data = jsonfield.JSONField(null=True, blank=True)

    def __str__(self: "DocumentSet") -> str:
        return str(self.document_name)


class CustomeUser(AbstractUser):
    """Model for saving basic user info."""

    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(
        verbose_name="user_email", max_length=255, null=True, blank=True
    )

    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self: "CustomeUser") -> str:
        return str(self.username)

    class Meta:
        unique_together = ["email"]

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        related_name='custom_users_user_permissions'
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        related_name='custom_users_groups'
    )


class Customer(models.Model):
    surname = models.CharField(max_length=250, null=True, blank=True)
    firstName = models.CharField(max_length=250, null=True, blank=True)
    nationality = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="customer_country",
        null=True,
        blank=True,
    )
    gender = models.CharField(choices=gender, null=True, max_length=10)

    def __str__(self: "Customer") -> str:
        return str(self.firstName)


class FileUpload(models.Model):
    """Saves FIle in model."""

    file = models.FileField(upload_to="uplaods/file/", null=False, blank=False)
    is_active = models.BooleanField(default=True)
    userImage = models.ForeignKey(
        CustomeUser,
        on_delete=models.SET_NULL,
        related_name="user_image",
        null=True,
        blank=True
    )

    def delete_file(self: 'FileUpload') -> None:
        """Delete file."""
        self.delete()
