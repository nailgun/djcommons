from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        if self.parent:
            return u'%s: %s' % (self.parent, self.name)
        else:
            return self.name
