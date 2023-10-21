from django.contrib.auth.models import BaseUserManager


class NewUserAccountManager(BaseUserManager):

    def create_superuser(self, name, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        user = self.create_user(name=name, email=email, password=password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, name, email, password, **other_fields):
        if not email:
            raise ValueError('Email address is required!')

        if not name:
            raise ValueError('Please enter your name')

        email = self.normalize_email(email)
        if password is not None:
            user = self.model(email=email, name=name, password=password, **other_fields)
            user.save()
        else:
            user = self.model(email=email, name=name, password=password, **other_fields)
            user.set_unusable_password()
            user.save()
        return user
