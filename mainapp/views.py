from django.shortcuts import render
from django.views.generic import View
from datetime import date, datetime

from sklearn.tree import DecisionTreeClassifier

from visitorapp.views import booking_page
from .forms import *


def index(request):
    if request.user.username != '':
        userr = request.user.username
    else:
        userr = 'Login'
    return render(request, "mainapp/index.html", context={'user': userr})


def contact_page(request):
    if request.user.username != '':
        userr = request.user.username
    else:
        userr = 'Login'
    return render(request, "mainapp/contact_page.html", context={'user': userr})


def train_model(data):
    cls = DecisionTreeClassifier()
    features = [[1]] * len(data)
    cls.fit(features, data)
    predict = cls.predict([[1]])[0]
    return predict


def machine_learning(request):
    vistor = Visitor.objects.get(user__username=request.user.username)
    bar = BarOrder.objects.filter(visitor=vistor)
    typedrinks = []
    if len(bar):
        for b in bar:
            typedrinks.append(b.type_alcohole)
    else:
        for b in BarOrder.objects.all():
            typedrinks.append(b.type_alcohole)
    print(typedrinks)
    toptypedrinks = train_model(typedrinks)
    the_drinks = Bar.objects.filter(type_of_drink=toptypedrinks)
    return the_drinks


def bar_page_recomendation(request):
    bar = machine_learning(request)
    userr = request.user.username
    vistor = Visitor.objects.get(user__username=request.user.username)
    date_today = date(datetime.today().year, datetime.today().month, datetime.today().day)
    bookings = Booking.objects.filter(visitor=vistor)
    for book in bookings:
        if book.arrival_date <= date_today <= book.depature_date:
            try:
                room = Room.objects.get(number=book.number_room).number

            except:
                room = 'you do not live in our hotel'
            break
    return render(request, "barapp/bar.html", context={'bar': bar, 'user': userr, 'room': room})


def bar_page(request):
    bar = Bar.objects.all()
    userr = request.user.username
    vistor = Visitor.objects.get(user__username=request.user.username)
    date_today = date(datetime.today().year, datetime.today().month, datetime.today().day)
    bookings = Booking.objects.filter(visitor=vistor)
    for book in bookings:
        if book.arrival_date <= date_today <= book.depature_date:
            try:
                room = Room.objects.get(number=book.number_room).number

            except:
                room = 'you do not live in our hotel'
            break
    return render(request, "barapp/bar.html", context={'bar': bar, 'user': userr, 'room': room})


def post_bar_page(request, number):
    bar = Bar.objects.get(id=number)
    vistor = Visitor.objects.get(user__username=request.user.username)
    date_today = date(datetime.today().year, datetime.today().month, datetime.today().day)
    bookings = Booking.objects.filter(visitor=vistor)
    for book in bookings:
        if book.arrival_date <= date_today <= book.depature_date:
            bar.num_room.add(Room.objects.get(number=book.number_room))
            bar.visitors.add(vistor)
            BarOrder.objects.create(visitor=vistor, type_alcohole=bar.type_of_drink)
            break

    return bar_page(request)


def filter_bar_page(request, type_alcohol):
    bar = Bar.objects.filter(type_of_drink=type_alcohol)
    userr = request.user.username
    vistor = Visitor.objects.get(user__username=request.user.username)
    date_today = date(datetime.today().year, datetime.today().month, datetime.today().day)
    bookings = Booking.objects.filter(visitor=vistor)
    for book in bookings:
        if book.arrival_date <= date_today <= book.depature_date:
            try:
                room = Room.objects.get(number=book.number_room).number

            except:
                room = 'you do not live in our hotel'
            break
    return render(request, "barapp/bar.html", context={'bar': bar, 'user': userr, 'room': room})


class BookingCreate(View):
    def get(self, request, type_room, count_person):
        from loginapp.views import LoginFormView
        if request.user.username == '':
            return LoginFormView.as_view()(request)
        dictdata = {'type_room': type_room, 'count_person': count_person}
        form = BookingForm(initial=dictdata)
        return render(request, 'mainapp/booking.html', context={'form': form})

    def post(self, request, type_room, count_person):
        bound_form = BookingForm(request.POST)

        if bound_form.is_valid():
            bound_form.save(Visitor.objects.get(user__username=request.user.username))

            return booking_page(request)
        return render(request, 'mainapp/booking.html', context={'form': bound_form})
