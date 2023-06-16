from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.conf import settings

def upload_path(instance,filename):
    ext = filename.split('.')[-1]
    return '/'.join(['image',str(instance.userPro.id)+str(instance.nickName)+'.'+ext])


# Create your models here.
class UserManager(BaseUserManager):
    
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    
    email = models.EmailField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    nickName = models.CharField(max_length=30)
    userPro = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='userPro',on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True,null=True,upload_to=upload_path)

    def __str__(self):
        return self.nickName

class FriendRequest(models.Model):
    askFrom = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='askFrom',on_delete=models.CASCADE)
    askTo = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='askTo',on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    class Meta:
        unique_together = (('askFrom','askTo'),)
    
    def __str__(self):
        return f"{self.askFrom} ----> {self.askTo}"

class Message(models.Model):
    message = models.CharField(max_length=150)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='receiver',on_delete=models.CASCADE)

    def __str__(self):
        return self.sender