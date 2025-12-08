from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Note


@login_required
def index(request, ):
    note_list = Note.objects.filter(owner=request.user).order_by("-save_date")
    context = { "note_list": note_list }
    return render(request, "pages/index.html", context)

def note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(
        request,
        "pages/note.html",
        {"note": note}
    )

def add(request):
    try:
        new_note = request.POST["note_text"]
        if new_note == "":
            return redirect("/")
    except(KeyError):
        return redirect("/")
    else:
        added_note = Note(owner=request.user, note_text=new_note, save_date=timezone.now())
        added_note.save()
        return redirect("/")
