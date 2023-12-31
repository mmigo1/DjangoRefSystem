from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        user = self.create_user(phone, password, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, phone, password, **other_fields):

        if not phone:
            raise ValueError('Phone address is required!')
        if password is not None:
            user = self.model(phone=phone, password=password, **other_fields)
            user.save()
        else:
            user = self.model(phone=phone, password=password, **other_fields)
            user.set_unusable_password()
            user.save()
        return user

    def get_by_natural_key(self, phone):
        return self.get(phone=phone)
