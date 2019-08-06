from django.db import models


# Create your models here.

class BookInfo(models.Model):
    btitle = models.CharField(max_length=64)
    bpub_date = models.DateField()


class HeroInfo(models.Model):
    hname = models.CharField(max_length=64)
    hgender = models.BooleanField()
    hcomment = models.TextField()
    hbook = models.ForeignKey('BookInfo',on_delete=models.CASCADE)
