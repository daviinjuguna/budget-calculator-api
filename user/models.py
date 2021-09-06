from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('phone number is required')
        if not password:
            raise ValueError('password is required')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,


        )
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('staff', False)
        extra_fields.setdefault('admin', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('admin') is not True:
            raise ValueError('Superuser must have admin=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")

    phone = models.CharField(
        max_length=15, verbose_name="Phone", validators=[phone_regex], unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    name = models.CharField(
        max_length=100, verbose_name="Name", default="")

    def __str__(self):
        return self.name

# income streams


class Income(models.Model):
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    income = models.CharField(max_length=100, verbose_name="Income stream")
    amount = models.FloatField(default=0, verbose_name="Amount",)

    def __str__(self):
        return self.income


class Expense(models.Model):
    user = models.ForeignKey(User, verbose_name="user",
                             on_delete=models.CASCADE)
    expense = models.CharField(max_length=100, verbose_name="Expense Type",)

    amount = models.FloatField(
        default=0, verbose_name="Amount", blank=True, null=True)
    static = models.BooleanField(default=False, verbose_name="is static")
    recommended = models.FloatField(
        default=0, verbose_name="Recommended %", max_length=10)

    def __str__(self):
        return self.expense
