from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """ Manager to creare user / super user for custom class """
    def create_user(self, email, password=None, first_name=None, last_name=None):
        user = self.model(
            email=email.lower(),
            first_name=first_name,
            last_name=last_name,
        )
        user_password = password
        if user_password is None:
            user_password = self.make_random_password()
        user.set_password(user_password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user