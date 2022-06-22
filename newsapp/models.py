from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
# Create your models here.
    
class Source(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.id
    

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = CountryField(multiple=True)
    tag = TaggableManager()
    source = models.ManyToManyField(Source)
    def __str__(self):
        return self.user.username
    
class Newsfeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsfeed = models.TextField()
    
    def __str__(self):
        return self.user.username