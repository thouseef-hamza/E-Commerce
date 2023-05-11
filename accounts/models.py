from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager 
# Create User models here.

# class CustomUserManager(BaseUserManager):
#     def _create_user(self,email, password,first_name,last_name,mobile, **extra_fields):
#         if not email:
#             raise ValueError('Email Must Be Provided')
#         if not password:
#             raise ValueError('Password Is Not Provided')
        
#         user = self.model(
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             mobile = mobile,
#             **extra_fields
#         )
        
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
        
    
#     def create_user(self, email, password,first_name,last_name,mobile, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_active", True)
#         extra_fields.setdefault("is_superuser",False)
#         return self._create_user(email, password,first_name,last_name,mobile,password **extra_fields)

#     def create_superuser(self,email, password,first_name,last_name,mobile, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_active", True)
#         extra_fields.setdefault("is_superuser", True)

#         return self._create_user(email, password,first_name,last_name,mobile,password **extra_fields)

        
        
    


# class  User(AbstractBaseUser,PermissionsMixin):
    
#     email = models.EmailField(db_index=True,unique=True,max_length=254)
#     first_name = models.CharField(max_length=240)
#     last_name = models.CharField(max_length=255)
#     mobile = models.CharField(max_length=50)
#     address = models.CharField(max_length=250)
    
#     is_staff = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)
    
#     objects = CustomUserManager()
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name','last_name','mobile']
    
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
        
class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User Must Have An Email Address')
        
        if not username:
            raise ValueError('User Must Have An Username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,first_name,last_name,email,username,password):
        user = self.create_user(
           email=self.normalize_email(email),
           username=username,
           password=password,
           first_name=first_name,
           last_name=last_name,
        ) 
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
        
        
        
        
        
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=13)
    
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects  = MyAccountManager()
    
    def __str__(self):
        return self.email
    
    
    # if the superuser, he has the permission to change
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    
    def has_module_perms(self,add_label):
        return True 
    
