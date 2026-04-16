from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Note


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "pages/signup.html"

@login_required
def index(request):
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

def delete(request, note_id):
    Note.objects.filter(pk=note_id).delete()
    return redirect("/")
