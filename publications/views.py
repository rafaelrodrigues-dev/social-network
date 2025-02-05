from django.shortcuts import render
from publications.models import Publication

def home(request):
    publications = Publication.objects.all()
    return render(request,'publications/pages/home.html',{
        'publications':publications
        })
