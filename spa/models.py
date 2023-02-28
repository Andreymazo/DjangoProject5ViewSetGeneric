from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from pkg_resources import _
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

NULLABLE = {'blank': True, 'null': True}
# UserManager
# class CustomUserManager(UserManager):
#
#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#
#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         return self._create_user(email, password, **extra_fields)
#
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("The given email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.password = make_password(password)
#         user.save(using=self._db)
#         return user

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    # firstname = models.CharField(max_length = 60)
    # lastname = models.CharField(max_length = 60)
    email = models.EmailField(max_length = 240, unique=True)
    # phone = PhoneNumberField(null=True, blank=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length = 240)
    is_staff = models.BooleanField(_('staff status'), default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']#'firstname', 'lastname',

    objects = CustomUserManager()
    # user_permissions = None
    # groups = None
    def __str__(self):
        return self.email


# class User(AbstractUser):
    # objects = CustomUserManager()

    # verify_token = models.CharField(max_length=35, verbose_name='Токен верификации',
    #                                 **NULLABLE)
    # verify_token_expired = models.DateTimeField(**NULLABLE,
    #                                             verbose_name='Дата истечения токена')
    # new_password = models.CharField(verbose_name="новый пароль", max_length=128, **NULLABLE)
    # username = None
    # email = models.EmailField(
    #     verbose_name='Почта',
    #     unique=True
    # )
    # phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    # city = models.CharField(max_length=35, verbose_name='город',**NULLABLE)
    # avatar = models.ImageField(upload_to='media/', verbose_name='аватарка',**NULLABLE)
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    # def __str__(self):
    #         return f'{self.email} '#{self.avatar} {self.city}{self.phone}

class Lesson(models.Model):
    name = models.CharField(max_length=35, verbose_name='название урока', **NULLABLE)
    preview = models.CharField(max_length = 50)
    smth = models.ForeignKey('spa.Course',on_delete=models.CASCADE, related_name='smthin', **NULLABLE)
    description = models.CharField(max_length=350, verbose_name='описание урока', **NULLABLE)
    reference = models.CharField(max_length=55, **NULLABLE, verbose_name='ссылка на видео')


    class Meta:
        verbose_name='урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.smth} {self.name}{self.preview}   {self.reference}'#{self.description}


class Course(models.Model):
    name = models.CharField(max_length=35, verbose_name='название курса', **NULLABLE)
    preview = models.CharField(max_length=50, verbose_name=' фото урока', **NULLABLE)
    description = models.TextField(max_length=300, verbose_name='описание курса', **NULLABLE)


    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
            return f'{self.name}{self.preview}  {self.description}'
    # default_permission = [AllowAny]
    # permissions = {
    #     "list": [IsAuthenticated],
    #     "retrieve": [IsAdminUser]
    # }
    # def get_permissions(self):
    #     return [perm() for perm in self.permissions.get(self.action, self.default_permission)]

class Payment(models.Model):
    PAYMENT_CARD = 'card'
    PAYMENT_CASH = 'cash'
    PAY_FORMS = (
        (PAYMENT_CARD, 'перевод на счет'),
        (PAYMENT_CASH, 'наличные')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE)#settings.AUTH_USER_MODEL,
    date_of_payment = models.DateTimeField(verbose_name='дата оплаты', **NULLABLE)
    lesson = models.ForeignKey('spa.Lesson', on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    course = models.ForeignKey('spa.Course', on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    sum_of_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='сумма оплаты')
    form_of_payment = models.CharField(max_length=10, choices=PAY_FORMS, default=PAYMENT_CARD, verbose_name='способ оплаты наличные или перевод')

    def __str__(self):
        return f'{self.user} {self.sum_of_payment}'


    class Meta:
        verbose_name='платеж'
        verbose_name_plural = 'платежи'


PERIOD_DAY = 86400
PERIOD_WEEK = 604800
PERIOD_MONTH = 2419200

PERIODS = (
        (PERIOD_DAY, 'день=86400'),
        (PERIOD_WEEK, 'неделя=604800'),
        (PERIOD_MONTH, 'месяц=2419200'),
    )
STATUS_DONE = False
STATUS_START = True

STATUSES = (
        (STATUS_DONE, False),
        (STATUS_START, True),
    )
class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(choices=STATUSES, default=STATUS_START)
    subscribed_on = models.DateTimeField(auto_now_add=True)##auto_created=?????????
    period = models.TimeField(auto_now=True, max_length=10, choices=PERIODS, **NULLABLE)

