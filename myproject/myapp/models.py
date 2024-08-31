from django.db import models
import random

class account(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    account_number = models.CharField(max_length=14, unique=True, blank=True, editable=True)  # Custom primary key
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='photos/')
    date = models.DateField()
    terms_accepted = models.BooleanField(default=False)
    generated_number = models.CharField(max_length=12, null=True, blank=True)
    pin = models.CharField(max_length=6, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = f"082322{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fname} {self.lname}"
