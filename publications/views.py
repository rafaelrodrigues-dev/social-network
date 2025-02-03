from django.shortcuts import render

def home(request):
    return render(request,'publications/pages/home.html')
