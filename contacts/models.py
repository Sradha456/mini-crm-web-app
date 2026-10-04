from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Deal(models.Model):
    STAGE_CHOICES = [
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    ]

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    title = models.CharField(max_length=200)

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES,
        default='New'
    )

    def __str__(self):
        return self.title