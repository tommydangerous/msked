from datetime import timedelta
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone

from locations.models import Location

class Station(models.Model):
    created  = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location)
    name     = models.CharField(max_length=30, unique=True)
    slug     = models.SlugField(blank=True, null=True, unique=True)

    def __unicode__(self):
        return 'Station %s' % self.name

    def number(self):
        try:
            num = int(self.name)
        except ValueError:
            num = None
        return num

    def numerical_name(self):
        try:
            num = int(self.name)
        except ValueError:
            num = None
        return num

    def recent_note(self):
        """Return the most recent note."""
        notes = self.note_set.order_by('-created')
        if notes:
            note = notes[0]
            now  = timezone.now()
            day  = int(now.strftime('%w'))
            if note.updated > (now - timedelta(days=day)):
                return note

    def seats(self):
        return self.seat_set.all().order_by('name')

    def save(self, *args, **kwargs):
        words = self.name.split(' ')
        name = []
        for word in words:
            name.append(word.lower().capitalize())
        self.name = ' '.join(name)
        self.slug = slugify(self.name)
        super(Station, self).save(*args, **kwargs)