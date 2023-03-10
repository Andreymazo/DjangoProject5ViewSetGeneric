from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from pkg_resources import _
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

import spa

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
    email = models.EmailField(max_length=240, unique=True)
    # phone = PhoneNumberField(null=True, blank=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=240)
    is_staff = models.BooleanField(_('staff status'), default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']  # 'firstname', 'lastname',

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
    preview = models.CharField(max_length=50, **NULLABLE)
    smth = models.ForeignKey('spa.Course', on_delete=models.CASCADE, related_name='smthin', **NULLABLE)
    description = models.CharField(max_length=350, verbose_name='описание урока', **NULLABLE)
    reference = models.CharField(max_length=55, **NULLABLE, verbose_name='ссылка на видео')
    price = models.IntegerField(default=1000)

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.name} {self.description}{self.smth} '  ## {self.reference}{self.preview}


class Course(models.Model):
    name = models.CharField(max_length=35, verbose_name='название курса', **NULLABLE)
    preview = models.CharField(max_length=50, verbose_name=' фото урока', **NULLABLE)
    description = models.TextField(max_length=300, verbose_name='описание курса', **NULLABLE)
    pro_file = models.ForeignKey('spa.Profile', on_delete=models.CASCADE, **NULLABLE)

    # pro_file = GenericRelation('profile')##Dostup k profile cherez Course

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
        return f'{self.name}{self.preview}  {self.description}'


# def check_for_change(instance):
#     try:
#         course = Course.objects.get(id=instance.id)
#     except Course.DoesNotExist:
#         return  None
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

    pro_filee = models.ForeignKey('spa.Profile', verbose_name='пользователь', on_delete=models.CASCADE, default=0,
                                  db_constraint=False)  # settings.AUTH_USER_MODEL,
    date_of_payment = models.DateTimeField(verbose_name='дата оплаты', **NULLABLE)
    lesson = models.ForeignKey('spa.Lesson', on_delete=models.CASCADE, related_name="lesson", verbose_name='урок',
                               **NULLABLE, db_constraint=False)  # db_constraint=False
    course = models.ForeignKey('spa.Course', on_delete=models.CASCADE, related_name="course", verbose_name='курс',
                               **NULLABLE, db_constraint=False)
    sum_of_payment = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='сумма оплаты')
    form_of_payment = models.CharField(max_length=10, choices=PAY_FORMS, default=PAYMENT_CARD,
                                       verbose_name='способ оплаты наличные или перевод')
    # PaymentURL = models.CharField(max_length=50, verbose_name= "ссылка на оплату")
    Success = models.CharField(max_length=50, verbose_name="Статус обработки", null=True)
    ErrorCode = models.CharField(max_length=50, verbose_name="Ошибка", null=True)
    Message = models.CharField(max_length=50, verbose_name="Сообщение", null=True)
    Details = models.CharField(max_length=50, verbose_name="Детали", null=True)
    TerminalKey = models.CharField(max_length=50, verbose_name="Детали", null=True)
    Status = models.CharField(max_length=50, verbose_name="Детали", null=True)
    PaymentId = models.CharField(max_length=50, verbose_name="Номер платежа", null=True)
    OrderId = models.CharField(max_length=50, verbose_name="Номер заказа", null=True)
    Amount = models.CharField(max_length=50, verbose_name="Сумма", null=True)
    PaymentURL = models.CharField(max_length=50, verbose_name="Ссылка на оплату", null=True)

    def __str__(self):
        return f' {self.sum_of_payment}'  # {self.pro_filee}

    class Meta:
        verbose_name = 'платеж'
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
    profile = models.ForeignKey('spa.Profile', on_delete=models.CASCADE)  ##Nelzya FK esli uzhe est M2M???
    course_subscribe = models.ForeignKey('spa.Course', on_delete=models.CASCADE, **NULLABLE)
    lesson_subscribe = models.ForeignKey('spa.Lesson', on_delete=models.CASCADE, **NULLABLE)
    status = models.BooleanField(choices=STATUSES, default=STATUS_START)  ##Podpisan ili net
    status_send = models.BooleanField(choices=STATUSES, default=STATUS_START)  ##Otoslano ili net
    subscribed_on = models.DateTimeField(auto_now_add=True)  ##auto_created=?????????
    period = models.TimeField(auto_now=True, max_length=10, choices=PERIODS, **NULLABLE)

    class Meta:
        # ordering = ('user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.profile} {self.course_subscribe} {self.lesson_subscribe} {self.status} {self.subscribed_on} {self.period}'


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Профиль', on_delete=models.CASCADE)
    email = models.CharField(max_length=240, unique=False, **NULLABLE)
    title = models.CharField(max_length=60, verbose_name='наименование')
    slug = models.SlugField(verbose_name='Персональная ссылка', unique=True, max_length=255, **NULLABLE)
    bio = models.TextField(max_length=500, verbose_name='Информация о себе', blank=True)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)###Tri polya sviazivaut Profile so vsemi modeliami voobshe
    # content_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    avatar = models.ImageField(
        verbose_name='Аватар профиля',
        blank=True,
        upload_to='media/',
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg'))
        ]
    )
    date_birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    # following_subscription = models.ManyToManyField('spa.UserSubscription', verbose_name='Подписки',
    #                                                 related_name='followers', **NULLABLE)##M2M tut ne podhodit, prosto FK
    # following_payment = models.ManyToManyField('spa.Payment', verbose_name='Платежи', related_name='followers_payments',
    #                                            symmetrical=False, **NULLABLE)

    def __str__(self):
        return f'{self.title} '  # {self.user} {self.slug} {self.following_subscription} {self.following_payment}

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица данными
        """
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super().save(*args, **kwargs)

        # db_table = 'app_profiles'

    # @property
    # def get_avatar(self):
    #     """
    #     Получение аватара при отсутствии загруженного
    #     """
    #     if not self.avatar:
    #         return f'https://ui-avatars.com/api/?size=128&background=random&name={self.user.username}'
    #     return self.avatar.url

    # @property
    # def get_age(self):
    #     """
    #     Вычисление возраста пользователя
    #     """
    #     return (date.today() - self.date_birthday) // timedelta(days=365.2425)

    # def get_absolute_url(self):
    #     """
    #     Ссылка на профиль
    #     """
    #     return reverse('spa:profile', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})


# def save(self, *args, **kwargs):
#      """
#      Сохранение параметров модели при их отсутствии заполнения
#      """
#      if not self.slug:
#          self.slug = unique_slugify(self, self.user.username)
#      if self.slug:
#          self.slug = self.slug.lower()
#      super().save(*args, **kwargs)
#
#  def __str__(self):
#      """
#      Возвращение имени пользователя
#      """
#      return self.user.username

###Signals are not allowed by Oleg
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_user_profile(sender, instance, created, **kwargs):
#     """
#     Сигнал создания профиля пользователя
#     """
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     """
#     Сигнал пересохранения профиля пользователя
#     """
#     instance.profile.save()
class Mailinglog(models.Model):
    mailing = models.CharField(max_length=100, verbose_name='Email')
    result = models.CharField(max_length=100, verbose_name='Result')
    last_attempt = models.DateTimeField(auto_now=True)
