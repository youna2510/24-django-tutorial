from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    student_number = models.CharField(max_length=8, null=True, verbose_name="학번")

    class Meta:
        db_table = "user"
        verbose_name = "유저"


class Study(models.Model):
    name = models.CharField(max_length=500, verbose_name="스터디 이름")
    description = models.CharField(max_length=2000, verbose_name="스터디 설명")

    class Meta:
        db_table = "study"
        verbose_name = "스터디"
