from django import forms
from django.forms import widgets, SelectDateWidget
from django.core.exceptions import ValidationError

from .models import *


class BookingForm(forms.Form):
    #type_room = forms.ChoiceField(choices=(("standart", "standart"), ("premium", "premium"), ('vip', "vip")))
    type_room = forms.CharField(initial='vip')
    count_person = forms.IntegerField()

    arrival_dates = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}))
    depature_dates = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'}))
    promocode = forms.CharField(max_length=15, required=False)
    type_room.widget.attrs.update({'class': 'form-control form-group'}, id="exampleFormControlSelect1")
    count_person.widget.attrs.update({'class': 'form-control'})
    promocode.widget.attrs.update({'class': 'form-control'})



    def clean_promocode(self):
        if self.cleaned_data['promocode'] != '':
            try:
                promocod = Promocod.objects.get(key=self.cleaned_data['promocode'])
            except:
                raise ValidationError('wrong promo code')
        else:
            return self.cleaned_data['promocode']




    def clean(self):
        try:
            room = Room.objects.get(type_room=self.cleaned_data['type_room'],
                                    count_person=int(self.cleaned_data['count_person']))
        except:
            raise ValidationError('incorrect data')
        arrival_date = date(self.cleaned_data['arrival_dates'].year, self.cleaned_data['arrival_dates'].month,
                            self.cleaned_data['arrival_dates'].day)

        depature_date = date(self.cleaned_data['depature_dates'].year, self.cleaned_data['depature_dates'].month,
                             self.cleaned_data['depature_dates'].day)
        room = Room.objects.get(type_room=self.cleaned_data['type_room'],
                                count_person=int(self.cleaned_data['count_person']))

        if arrival_date < date(datetime.today().year, datetime.today().month, datetime.today().day):
            raise ValidationError('Dear visitor, this date has already passed')

        if arrival_date >= depature_date:
            raise ValidationError('Date is incorrect')

        if not room.room_availability(arrival_date, depature_date):

            raise ValidationError('The room is already booked for these dates')


    def save(self, user: Visitor):
        print()
        print()
        print('save')
        print(self.cleaned_data['promocode'])
        print()
        print()
        number = user.room_reservation(self.cleaned_data['type_room'], int(self.cleaned_data['count_person']),
                                       self.cleaned_data['arrival_dates'], self.cleaned_data['depature_dates'],
                                       self.cleaned_data['promocode'])

        if number:
            return Booking.objects.get(number_booking=number)
