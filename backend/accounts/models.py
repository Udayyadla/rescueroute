from django.db import models
from django.contrib.auth.models import AbstractUser     

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        DONOR = "DONOR", "Donor"
        CHARITY = "CHARITY","Charity"
        VOLUNTEER = "VOLUNTEER", "Volunteer"
        ADMIN = "ADMIN", "Admin"
    role = models.CharField(
        max_length=20,
        choices = Role.choices,
        default= Role.DONOR,)
    phone_number = models.CharField(max_length=15,blank=True)

    def __str__(self):
        return self.username