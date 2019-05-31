from django.shortcuts import render
from mainapp.models import *

def booking_page(request):
    vistor = Visitor.objects.get(user__username=request.user.username)
    bookings = Booking.objects.filter(visitor=vistor)
    rooms = Room.objects.all()
    user = request.user.username
    return render(request, 'visitorapp/visitor_bookingpage.html', context={'bookings': bookings, 'rooms':rooms, 'user': user}, )


def post_booking_page(request, number_booking):
    booking = Booking.objects.get(number_booking=number_booking)
    arrivaldate = booking.arrival_date
    depaturedate = booking.depature_date
    number_room = booking.number_room
    booking.delete()

    room = Room.objects.get(number=number_room)

    room.arrival_dates.remove(Data.objects.filter(data=arrivaldate)[0])
    room.depature_dates.remove(Data.objects.filter(data=depaturedate)[0])

    return booking_page(request)


def visitor_page(request):
    vistor = Visitor.objects.get(user__username=request.user.username)
    return render(request,'visitorapp/visitor_page.html', context={'visitor': vistor})