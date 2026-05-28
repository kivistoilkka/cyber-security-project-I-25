from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import Http404
from django.db import connection

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

# @login_required # Flaw1
def note(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    # if request.user != note.owner: # Flaw1
    #     raise Http404("No Note matches the given query.") # Flaw1

    return render(
        request,
        "pages/note.html",
        {"note": note}
    )

# @login_required # Flaw1
def add(request):
    try:
        new_note = request.POST["note_text"]
        if new_note == "":
            return redirect("/")
    except(KeyError):
        return redirect("/")
    else:
        added_note = Note(owner=request.user, note_text=new_note, save_date=timezone.now(), update_time=timezone.now())
        added_note.save()
        return redirect("/")

# @login_required # Flaw1
def delete(request, note_id):
    Note.objects.filter(pk=note_id).delete()

    # try: # Flaw1
    #     note = Note.objects.get(pk=note_id) # Flaw1
    # except Note.DoesNotExist: # Flaw1
    #     return redirect("/") # Flaw1
    # if request.user == note.owner: # Flaw1
    #     note.delete() # Flaw1

    return redirect("/")

# @login_required # Flaw1
def update(request, note_id):
    updated_note = request.POST["note_text"]

    # note = get_object_or_404(Note, pk=note_id) # Flaw1 # Flaw2
    # if request.user != note.owner: # Flaw1
    #     raise Http404("No Note matches the given query.") # Flaw1

    query = 'UPDATE pages_note SET update_time = datetime(\'now\'), note_text = "' + updated_note + '" WHERE id = ' + str(note_id)
    with connection.cursor() as cursor:
        cursor.execute(query)

    # note.note_text = updated_note # Flaw2
    # note.save() # Flaw2

    return redirect(f"/note/{note_id}")

# @login_required # Flaw1
def search(request):
    filters = {
        "owner": request.user,
        **request.GET.dict(),
    }

    # allowed_filters = {'note_text'} # Flaw5
    # clean_filters = {k: v for k, v in request.GET.items() if k in allowed_filters} # Flaw5
    # filters = { # Flaw5
    #     "owner": request.user, # Flaw5
    #     **clean_filters, # Flaw5
    # } # Flaw5

    note_list = Note.objects.filter(**filters).order_by("-save_date")
    context = { "note_list": note_list }
    return render(request, "pages/search.html", context)
