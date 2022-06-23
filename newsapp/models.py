from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from taggit.managers import TaggableManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
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
    
    


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
       
        "Password Reset for {title}".format(title="Some website title"),   
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )