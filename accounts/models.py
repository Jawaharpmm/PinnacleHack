from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class CareTaker(models.Model): 
                      user = models.OneToOneField(User,on_delete=models.CASCADE)
                      us_name = models.CharField(max_length=20,default="")
                      phone_number = models.CharField(max_length=13)
                      care_taker_name = models.CharField(max_length=20)
                      care_taker_email = models.CharField(max_length=30)
                      care_taker_no = models.CharField(max_length=13)


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
