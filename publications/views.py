from django.shortcuts import render
from publications.models import Publication
from django.shortcuts import get_object_or_404

def home(request):
    publications = Publication.objects.all()
    return render(request,'publications/pages/home.html',{
        'publications':publications
        })

def publication_detail(request,pk):
    publication = get_object_or_404(Publication,pk=pk)
    return render(request,'publications/pages/publication-detail.html',{
        'publication':publication,
        'is_detail':True,
    })