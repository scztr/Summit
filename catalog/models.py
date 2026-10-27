from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Mountain(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    height = models.PositiveIntegerField()
    description = models.TextField()
    image = models.URLField(blank=True)
    summit_view = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    mountain = models.ForeignKey(Mountain,on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    description = models.TextField()
    choices =[
        ("easy", "Легкий"),
        ("medium", "Середній"),
        ("hard", "Складний"),
    ]
    difficult = models.CharField(max_length=20, choices=choices)
    duration = models.PositiveIntegerField()
    source = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Stop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    name = models.CharField(max_length=150)
    altitude = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

class Org(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    organizer = models.ForeignKey(Org, on_delete=models.PROTECT)
    title = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    rent = models.BooleanField(default=False)
    rent_detail = models.TextField(blank=True)
    sherpa = models.BooleanField(default=False)
    support = models.TextField(blank=True)
    services = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    choices=[
    ("open", "Відкрите"),
    ("closed", "Закрите"),
    ("cancelled", "Скасоване"),
    ]
    status = models.CharField(max_length=20, default="open", choices=choices)

    def __str__(self):
        return self.title