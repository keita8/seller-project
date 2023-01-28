from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from versatileimagefield.placeholder import OnDiscPlaceholderImage
import os
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
import os
import random
import string
from PIL import Image
from django.conf.urls.static import static



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910207878)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"profile/avatar/{new_filename}/{final_filename}"





class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='adresse email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser

    # notice the absence of a "Password field", that is built in.
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    class Meta:
        verbose_name = 'compte'
        verbose_name_plural = 'comptes'
        
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_perm(self, perm, obj=None):
        return self.admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin






class Profile(models.Model):
    class Gender(models.TextChoices):
        HOMME = "Masculin", "Mr"
        FEMME = "Feminin", "Mme"

    gender = Gender.HOMME
    sex = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=Gender.choices,
        verbose_name="Genre",
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="Adresse email",
        related_name="profile",
    )
    lastname = models.CharField(max_length=100, verbose_name="Nom de famille", null=True, blank=True)
    firstname = models.CharField(max_length=100, verbose_name="Prénom", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Date de naissance", auto_now_add=False, null=True, blank=True)
    phone_number = PhoneNumberField(blank=True, null=True, verbose_name="Téléphone")
    bio = HTMLField(blank=True, null=True)
    avatar = VersatileImageField(
        "Photo de profil",
        # width_field="width",
        # height_field="height",
        upload_to=upload_image_path,
        ppoi_field="image_ppoi",
        validators=[FileExtensionValidator(["jpg", "png"])],
    )
    
    
    image_ppoi = PPOIField()
    
    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'
    
    @property
    def get_avatar(self):
        return self.image.url if self.image else static("static/avatar/avatar.png")



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()


post_delete.connect(delete_user, sender=Profile)
