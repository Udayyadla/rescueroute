from django.db import models
from django.contrib.auth.models import AbstractUser   
from django.conf import settings  

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


class Organization(models.Model):
    class Type(models.TextChoices):
        RESTAURANT = "restaurant","Restaurant"
        NGO ='ngo','NGO',
        BUSINESS =  'business','Business'
        OTHER = 'other','Other'
    name = models.CharField(max_length=200)
    organization_type = models.CharField(
        max_length=20,
        choices=Type.choices)
    address = models.TextField()
    is_verfied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class DonorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="donor_profile"
        )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="donors",
        null = True,
        blank=True

        )

    def __str__(self):
        return f"Donor : {self.user.username}"


class CharityProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="charity_profile")
    organization = models.ForeignKey(
            Organization,
            on_delete=models.PROTECT,
            related_name="charities",
            null = True,
            blank=True
    
            )
     
    def __str__(self):
        return f"Charity : {self.user.username}"


class VolunteerProfile(models.Model):
    class Transport(models.TextChoices):
        WALK = "walk","Walk"
        BIKE = 'bike','Bike'
        CAR = 'car', 'Car'
    user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="volunteer_profile")
    is_available = models.BooleanField(default=False)
    transport_mode = models.CharField(
                    max_length=25,
                    choices = Transport.choices,
                    default=Transport.WALK
                    )

    def __str__(self):
        return f"Volunteer: {self.user.username}"
    