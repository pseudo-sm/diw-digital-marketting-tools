from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Business(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    data_id = models.CharField(max_length=255,null=True,blank=True)
    location_rule = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Review(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    review = models.TextField()
    date = models.CharField(max_length=255)
    rating = models.FloatField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.review

class RegUser(User):

    upi_id = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class EmailAccounts(models.Model):

    id = models.AutoField(primary_key=True)
    email_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    otp = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(RegUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.email_id

class RateRequest(models.Model):

    email = models.ForeignKey(EmailAccounts,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)

    

class RealReview(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    business = models.ForeignKey(Business,on_delete=models.CASCADE)
    regUser = models.ForeignKey(RegUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name