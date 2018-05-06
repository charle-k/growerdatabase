from django.db import models

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_key(self):
        if self.province:
            t = self.name.strip().title() + self.province.name.strip().title()
        else:
            t = self.name.strip().title()
        return t

class Grower(models.Model):
    Grower_Number = models.CharField(max_length=8, unique=True)
    Grower_Name = models.CharField(max_length=200)
    National_ID = models.CharField(max_length=15, unique=True)
    Mobile_Number = models.CharField(max_length=20)
    District = models.ForeignKey(District, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['Grower_Name']

    def __str__(self):
        return self.name


class IdGenerator(models.Model):
    id_number = models.CharField(max_length=15, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
