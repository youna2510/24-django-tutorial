from django.db import models

# Create your models here.

class Study(models.Model):
    name = models.CharField(max_length=500, verbose_name="스터디 이름")
    description = models.CharField(max_length=2000, verbose_name="스터디 설명")

    class Meta:
        db_table = "study"
        verbose_name = "스터디"