from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

class Profile(models.Model):
    created     = models.DateTimeField(auto_now_add=True)
    login_count = models.IntegerField(default=1)
    slug        = models.SlugField(blank=True, null=True, unique=True)
    user        = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.user)

def create_profile(sender, instance, **kwargs):
    try:
        profile = Profile.objects.get(user=instance)
        profile.slug = slugify(instance.username)
        profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(slug=slugify(instance.username), user=instance)

post_save.connect(create_profile, sender=User)

User.profile = property(lambda u: u.profile_set.all()[0])