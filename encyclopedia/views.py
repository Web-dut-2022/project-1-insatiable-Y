import markdown2
import random
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown2.markdown(util.get_entry(entry)),
            "entry_title": entry.capitalize()
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page was not found."
        })

def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[query]))
        elif query is not None:
            entries  = util.list_entries()
            matches = []
            for entry in entries:
                if query.lower() in entry.lower():
                    matches.append(entry)
            if matches:
                return render(request, "encyclopedia/search.html", {
                    "entries": matches
                })
            else:
                return render(request, "encyclopedia/error.html",{
                    "message": "There were no results matching the query."
                })
        else:
            return HttpResponseRedirect("encyclopedia:index")

def newentry(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html",{
                    "message": "This page already exists!"
                })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
    return render(request, "encyclopedia/newentry.html")

def editentry(request, entry_title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(entry_title, content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=[entry_title]))
    else:
        return render(request, "encyclopedia/editentry.html", {
            "content": util.get_entry(entry_title),
            "entry_title": entry_title
        })

def randompage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[random_entry]))