from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products', default='pix.jpg')
    videofile = models.FileField(blank=True,null=True, upload_to='videos/',default='videos.mp4')


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'category'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    videofile = models.FileField(blank=True,null=True, upload_to='videos/',default='videos.mp4')
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', default='pix.jpg')
    price = models.FloatField()
    description = models.TextField()
    local = models.BooleanField()
    foreign = models.BooleanField()
    latest = models.BooleanField()
    wood=models.BooleanField(default=False)
    gold=models.BooleanField(default=False)
    diamond=models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Carousel(models.Model):
    image =models.ImageField(upload_to='carouselpix',default='carousel.jpg')
    comment=models.CharField(max_length=100)

    def __str__(self):
        return self.comment


class Payment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.IntegerField()
    pay_code=models.CharField(max_length=36,blank=True, null=True,)
    first_name=models.CharField(max_length=50,blank=True, null=True,)
    last_name=models.CharField(max_length=50,blank=True, null=True,)
    phone=models.CharField(max_length=50,blank=True, null=True,)
    title=models.CharField(max_length=100,  blank=True, null=True)
    paid = models.BooleanField(default=False)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    title = models.CharField(max_length=50)
    videofile = models.FileField(blank=True,null=True, upload_to='videos/',default='videos.mp4')
    dfee = models.FloatField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'member'
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Member'


class Deletemember(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name=models.CharField(max_length=50,blank=True, null=True)
    last_name=models.CharField(max_length=50,blank=True, null=True)
    phone=models.CharField(max_length=50, blank=True, null=True)
    title=models.CharField(max_length=100,  blank=True, null=True)
    fee=models.FloatField(blank=True, null=True)
    dfee=models.FloatField(blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
   
    def __str__(self):
        return self.user.username



class Membership(models.Model):
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    membership=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    fee = models.FloatField()
    pay_code=models.CharField(max_length=36)
    memeber_no=models.CharField(max_length=36)
   

    def __str__(self):
        return self.first_name

