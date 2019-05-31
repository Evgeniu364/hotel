from unicodedata import decimal

from django.db import models
from django.utils.timezone import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime


class Data(models.Model):
    data = models.DateField()

    def __str__(self):
        return str(self.data)


class Room(models.Model):
    number = models.IntegerField(unique=True)
    type_room = models.CharField(max_length=100)
    count_person = models.IntegerField()
    cost_per_night = models.DecimalField(max_digits=19, decimal_places=3)
    arrival_dates = models.ManyToManyField(Data, related_name='arrival_dates', blank=True)
    depature_dates = models.ManyToManyField(Data, related_name='depature_dates', blank=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return 'the room number - {}, her type - {}'.format(self.number, self.type_room)

    def room_availability(self, arrival_date, depature_date):
        count = self.depature_dates.all().count()
        room_arrival_dates = self.arrival_dates.all().order_by('data')
        room_depature_dates = self.depature_dates.all().order_by('data')
        if arrival_date >= room_depature_dates[count - 1].data:
            return True
        elif depature_date <= room_arrival_dates[0].data:
            return True
        else:
            for i in range(count - 1):
                if arrival_date >= room_depature_dates[i].data and depature_date <= room_arrival_dates[i + 1].data:
                    return True
        return False


class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=999, blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_visitor(sender, instance, created, **kwargs):
        if created:
            Visitor.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_visitor(sender, instance, **kwargs):
        instance.visitor.save()

    def __str__(self):
        return 'name - {}'.format(self.user.username)

    def room_reservation(self, type_room, countperson, arrival_date: datetime, depature_date: datetime, promocode):
        rooms = Room.objects.filter(type_room=type_room)
        print('promo')
        print(promocode)
        arrival_date = date(arrival_date.year, arrival_date.month, arrival_date.day)
        depature_date = date(depature_date.year, depature_date.month, depature_date.day)
        price = (depature_date - arrival_date)
        discont = 1
        if promocode != '':
            discont = 1 - (Promocod.objects.get(key=promocode).value / 100)
        for room in rooms:
            if room.room_availability(arrival_date, depature_date) and room.count_person == countperson:
                if Booking.objects.all().count():
                    number = Booking.objects.all()[Booking.objects.all().count() - 1].number_booking + 1
                else:
                    number = 1
                cost = float((int(price.days) * float(room.cost_per_night))) * discont
                Booking.objects.create(number_booking=number, arrival_date=arrival_date,
                                       depature_date=depature_date, number_room=room.number, visitor=self,
                                       promocode=promocode,
                                       price=cost, type_room=type_room)
                room.arrival_dates.add(Data.objects.create(data=arrival_date))
                room.depature_dates.add(Data.objects.create(data=depature_date))

                return number

        return -1


class Booking(models.Model):
    number_booking = models.IntegerField(unique=True)
    arrival_date = models.DateField()
    depature_date = models.DateField()
    number_room = models.IntegerField()
    type_room = models.CharField(max_length=100)
    price = models.FloatField()
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE)
    promocode = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return 'number booking - {} visitor - {}'.format(self.number_booking, self.visitor.user.username)


class Promocod(models.Model):
    key = models.CharField(max_length=15)
    value = models.FloatField()

    def __str__(self):
        return '{} - {}'.format(self.key, self.value)


class Bar(models.Model):
    name = models.CharField(max_length=50)
    type_of_drink = models.CharField(max_length=20, choices=(('non-alcoholic', 'non-alcoholic'),
                                                             ('beer', 'beer'),
                                                             ('wine', 'wine'),
                                                             ('cognac', 'cognac'),
                                                             ('whiskey', 'whiskey')
                                               )
                                      )
    price = models.FloatField()
    visitors = models.ManyToManyField(Visitor, related_name='visitors', blank=True)
    num_room = models.ManyToManyField(Room, related_name='num_room', blank=True)
    image = models.ImageField(upload_to="mainapp/img")


class BarOrder(models.Model):
    visitor = models.ForeignKey('Visitor', on_delete=models.CASCADE)
    type_alcohole = models.CharField(max_length=20)