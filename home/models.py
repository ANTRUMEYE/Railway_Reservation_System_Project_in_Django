from django.db import models

# Create your models here.
class Trains(models.Model):
    tno=models.CharField(primary_key=True,max_length=50)
    tname=models.CharField(max_length=50)
    rid=models.ForeignKey('Route',on_delete=models.CASCADE)

    def __str__(self):
        return self.tno

class Route(models.Model):
    rid=models.CharField(max_length=50)
    ostation=models.CharField(max_length=50)
    dstation=models.CharField(max_length=50)
    def __str__(self):
        return self.rid

class Station(models.Model):
    sid=models.CharField(primary_key=True,max_length=50)
    sname=models.CharField(max_length=50)
    def __str__(self):
        return self.sid


class RouteStation(models.Model):
    tno=models.ForeignKey('Trains',on_delete=models.CASCADE)
    sid=models.ForeignKey('Station',on_delete=models.CASCADE)
    rid=models.ForeignKey('Route',on_delete=models.CASCADE)
    order=models.IntegerField()
    atime=models.CharField(max_length=50)

class Reservation(models.Model):
    tno=models.ForeignKey('Trains',on_delete=models.CASCADE)
    user=models.CharField(max_length=50)
    nos=models.IntegerField()
    date=models.CharField(max_length=50)
    amt=models.IntegerField()
    cls=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    pnr=models.CharField(max_length=50)
    src=models.CharField(max_length=50)
    des=models.CharField(max_length=50)




class Payment(models.Model):
    pnr=models.CharField(max_length=50)
    user=models.CharField(max_length=50)
    amt=models.IntegerField()
    mtd=models.CharField(max_length=50)
    date=models.CharField(max_length=50)
    cancel=models.CharField(max_length=50)











