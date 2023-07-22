from django.db import models

#Create automatic one to one object profile
from django.db.models.signals import post_save
from django.dispatch import receiver
# Custom user & admin panel
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy



class MyUserManager(BaseUserManager):
    #custom login with email
    def _create_user(self, email, password, **extra_fields):

        #save user email and password
        if not email:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff Status'),
        default = False,
        help_text = gettext_lazy('Designates whether the user can login this site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        default = True,
        help_text = gettext_lazy('Designates whether this user should be treated as active. Unselect this instead of deleting accounts')

    )

    USERNAME_FIELD = 'email'
    object = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=200, blank=True)
    full_name = models.CharField(max_length=250, blank=True)
    first_address = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username + "'s Profile'"

    def is_fully_fillup(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
