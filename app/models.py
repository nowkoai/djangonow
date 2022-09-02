from django.db import models
from django.utils import timezone

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='メールアドレス',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin




class Neuron(models.Model):
    STATUS_CHOICES = [(1, '未完了'),(2, '作業中'),(3, '完了')]
    
    text = models.TextField()
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    pub_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

class Synapse(models.Model):
    parent_text_id = models.TextField()
    child_text_id = models.TextField()
    neuron = models.ForeignKey( Neuron, on_delete=models.CASCADE, null=True )

    def __str__(self):
        return self.text


class Task(models.Model):
    ## taskのタイトル
    title = models.CharField(max_length=255)
    ## taskの作成日
    created_at = models.DateField(auto_now_add=True)
    ## taskが完了したかどうか
    completed = models.BooleanField(default=False)
    ## インデント
    indent = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

  