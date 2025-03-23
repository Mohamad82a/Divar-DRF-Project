from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

from account.models import User


class Ad(models.Model):
    date_added = models.DateTimeField(_('date published'), default=now)
    title = models.CharField(_('title'), max_length=150)
    caption = models.TextField(_('caption'))
    image = models.ImageField(_('image'), upload_to='images/ads/%Y/%m/%d')
    is_public = models.BooleanField(_('is public'),default=False, help_text=_('Public Ads will be displayed ''in the api views.'))
    publisher = models.ForeignKey(User, blank=True, null=True, related_name='ads', on_delete=models.CASCADE, verbose_name=_('publisher'))

    class Meta:
        ordering = ('-date_added',)
        get_latest_by = 'date_added'
        verbose_name = _('ad')
        verbose_name_plural = _('ads')

    def __str__(self):
        return self.title