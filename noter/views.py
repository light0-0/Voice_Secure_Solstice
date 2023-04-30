from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from .models import *
from datetime import datetime


# Create your views here.

def show_all(request, name):
    obj = note.objects.filter(username = name).values()

    # print(obj)
    
    context = {'data': obj, 'name':name}
    return render(request, 'index.html', context)


def add_note(request, name):
    
    if request.method == "POST":

        
        noteName = request.POST.get('noteName')
        noteText = request.POST.get('noteText')

        date_string = datetime.today().strftime('%d %B %Y')


        obj = note(username = name ,note_name = noteName, note_text = noteText, date= date_string)
        obj.save()

        url = reverse('noter:home', args=[name])
        return redirect(url)

    return HttpResponse("UUUUUUUUUUU")


def fav_delete(request, name):
    if request.method == "POST":
        if 'delete_note' in request.POST:
            noteId = request.POST.get('delete_note')
            obj = note.objects.get(id = noteId)

            obj.delete()

            url = reverse('noter:home', args=[name])
            return redirect(url)
        
        elif 'fav' in request.POST:
            noteId = request.POST.get('fav')
            
            obj = note.objects.get(id = noteId)
            
            if obj.fav == "F":
                obj.fav = "T"

            else:
                obj.fav = "F"

            obj.save()

            url = reverse('noter:home', args=[name])
            return redirect(url)
