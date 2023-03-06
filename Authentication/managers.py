from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None,*args, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, *args,**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username, password=None,*args,**kwargs):
        return self.create_user(email,username,password,staff=True,is_superuser=True,*args,**kwargs)