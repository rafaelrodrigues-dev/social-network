from django.shortcuts import render
from publications.models import Publication

def home(request):
    publications = Publication.objects.all()
    return render(request,'publications/pages/home.html',{
        'publications':publications
        })

def publication_detail(request,pk):
    publication = Publication.objects.all().filter(pk=pk).first()
    return render(request,'publications/pages/publication-detail.html',{
        'publication':publication,
        'is_detail':True,
    })