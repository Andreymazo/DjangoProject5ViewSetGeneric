from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):# firstname, lastname, company,
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=True,
            # firstname=firstname,
            # lastname=lastname,

            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user