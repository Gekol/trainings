from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Entry(models.Model):
    date = models.DateField()
    distance = models.FloatField()
    duration = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Entries"

    def __str__(self):
        return str(self.date) + " " + str(self.distance) + " " + str(self.duration)