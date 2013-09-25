from django.db import models

class UpdateMessage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    status  = models.CharField(default='warning', max_length=255)
    viewed  = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.content)