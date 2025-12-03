from django.shortcuts import render, get_object_or_404

from .models import Note


def index(request):
    note_list = Note.objects.order_by("-save_date")
    context = {"note_list": note_list}
    return render(request, "pages/index.html", context)

def note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(
        request,
        "pages/note.html",
        {"note": note}
    )
