from django.shortcuts import render
from django.http import HttpResponse


# creating first function for index

def index(request):
	return render(request,'index.html');