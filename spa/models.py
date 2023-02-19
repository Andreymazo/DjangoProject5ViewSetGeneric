from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
NULLABLE = {'blank': True, 'null': True}

class CustomUserManager(UserManager):

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

class User(AbstractUser):
    objects = CustomUserManager()

    # verify_token = models.CharField(max_length=35, verbose_name='Токен верификации',
    #                                 **NULLABLE)
    # verify_token_expired = models.DateTimeField(**NULLABLE,
    #                                             verbose_name='Дата истечения токена')
    # new_password = models.CharField(verbose_name="новый пароль", max_length=128, **NULLABLE)
    username = None
    email = models.EmailField(
        verbose_name='Почта',
        unique=True
    )
    phone = models.CharField(max_length=20, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=35, verbose_name='город',**NULLABLE)
    avatar = models.ImageField(upload_to='media/', verbose_name='аватарка',**NULLABLE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
            return f'{self.email}{self.phone}{self.avatar}  {self.city}'

class Course(models.Model):
    name = models.CharField(max_length=35, verbose_name='название курса', **NULLABLE)
    preview = models.ImageField(upload_to='media/', **NULLABLE)
    description = models.TextField(max_length=300, verbose_name='описание курса', **NULLABLE)

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    def __str__(self):
            return f'{self.name}{self.preview}  {self.description}'

class Lesson(models.Model):
    name = models.CharField(max_length=35, verbose_name='название урока', **NULLABLE)
    preview = preview = models.ImageField(upload_to='media/', verbose_name='картинка к уроку', **NULLABLE)
    description = models.ForeignKey(Course, on_delete=models.CASCADE, max_length=350, verbose_name='описание урока', **NULLABLE)
    reference = models.FileField(upload_to='media/', **NULLABLE, verbose_name='ссылка на видео')


    class Meta:
        verbose_name='урок'
        verbose_name_plural = 'уроки'

    def __str__(self):
        return f'{self.name}{self.preview}  {self.description} {self.reference}'
class Payments(models.Model):
    client = models.CharField(max_length=35, verbose_name='пользователь', **NULLABLE)
    date_of_payment = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    object_of_payment = models.CharField(max_length=45, verbose_name='оплаченый курс или урок', **NULLABLE)
    sum_of_payment = models.IntegerField(**NULLABLE, verbose_name='сумма оплаты')
    form_of_payment = models.CharField(max_length=45, **NULLABLE, verbose_name='способ оплаты наличные или перевод')



    class Meta:
        verbose_name='платеж'
        verbose_name_plural = 'платежи'

    def __str__(self):
        return f'{self.client}{self.date_of_payment}  {self.object_of_payment} {self.sum_of_payment} {self.form_of_payment}'