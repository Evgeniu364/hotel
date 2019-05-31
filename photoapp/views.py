from django.shortcuts import render

def photo(request):
    return render(request, "photoapp/photoapp.html")