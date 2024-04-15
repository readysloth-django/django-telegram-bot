from django.db import models
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _


class BroadcastTask(models.Model):
    text = models.TextField(_('Text'))
    executed = models.BooleanField(_('Executed'), default=False, editable=False)

    class Meta:
        verbose_name = _('Broadcast task')
        verbose_name_plural = _('Broadcast tasks')

    def __str__(self):
        return self.text[:15]


class ScheduledBroadcastTask(BroadcastTask):
    date = models.DateTimeField(_('Date'))

    class Meta:
        verbose_name = _('Scheduled broadcast task')
        verbose_name_plural = _('Scheduled broadcast tasks')

    def __str__(self):
        return super().__str__()


class ScheduledPeriodicBroadcastTask(ScheduledBroadcastTask):
    time_delta = models.DurationField(_('Time delta'))

    class Meta:
        verbose_name = _('Scheduled periodic broadcast task')
        verbose_name_plural = _('Scheduled periodic broadcast tasks')

    def __str__(self):
        return '{snippet}: {date} [+{delta}] '.format(
            date=self.date,
            delta=self.time_delta,
            snippet=super().__str__())
