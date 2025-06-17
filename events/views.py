from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def events(reques):
    return HttpResponse("Welcom to Events App!")
