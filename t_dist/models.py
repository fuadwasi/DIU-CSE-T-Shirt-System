from django.db import models

# Create your models here.
class Students(models.Model):
    sID = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    givenby = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,default="not_taken")


class Mate:
    db_table = "students"