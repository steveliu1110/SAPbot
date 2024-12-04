from django.db import models

# Create your models here.

class Website(models.Model):
    url = models.URLField(max_length=200, unique=True)
    chunk_count = models.IntegerField()
    last_update = models.TextField()

    def __str__(self):
        return self.url