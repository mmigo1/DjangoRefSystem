from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .utils import generate_ref_code
from django.utils import timezone
from django.core.validators import RegexValidator
from .manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, max_length=15, validators=[RegexValidator(regex=r'[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}')])
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def natural_key(self):
        return (self.phone)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True)
    recommended_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='ref_by')
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone}-{self.code}"

    def get_recommended_profiles(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user]
        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)
