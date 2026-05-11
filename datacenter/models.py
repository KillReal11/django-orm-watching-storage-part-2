from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        leaving_time = localtime(value=self.leaved_at, timezone=None)
        entering_time = localtime(value=self.entered_at, timezone=None)
        delta = leaving_time - entering_time
        total_seconds_delta = int(delta.total_seconds())
        return total_seconds_delta

    def is_visit_long(self, minutes=60):
        return self.get_duration() > minutes * 60


def format_duration(duration):
    seconds_in_minute = 60
    seconds_in_hour = 3600
    hours_delta = duration//seconds_in_hour
    minutes_delta = (duration % seconds_in_hour) // seconds_in_minute
    seconds_delta = (duration % seconds_in_hour) % seconds_in_minute
    return f'{hours_delta:02d}:{minutes_delta:02d}:{seconds_delta:02d}'
