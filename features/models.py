from django.db import models

# Create your models here.
class Members(models.Model):
    username=models.CharField(max_length=250)
    password=models.CharField(max_length=16)
    email=models.CharField(max_length=250)
    number=models.CharField(max_length=10)

    def __str__(self):
        return self.username


