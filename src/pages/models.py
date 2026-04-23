from django.db import models

from django.contrib.auth.models import User


class Note(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    note_text = models.CharField(max_length=200)
    save_date = models.DateTimeField()
    update_time = models.DateTimeField()

    def __str__(self):
        return self.note_text