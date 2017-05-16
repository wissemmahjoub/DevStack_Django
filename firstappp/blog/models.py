from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    name= models.CharField(max_length=255)