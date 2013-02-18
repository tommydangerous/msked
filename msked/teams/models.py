from django.db import models

class Team(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.name