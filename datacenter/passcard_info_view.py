from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render
from django.utils.timezone import localtime
from django.utils.formats import date_format
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    print(passcard)
    # Программируем здесь
    visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    for visit in visits:
        entering_time = localtime(value=visit.entered_at, timezone=None)
        duration = visit.get_duration()
        formatted_duration = format_duration(duration)
        long_visit = visit.is_visit_long()
        specific_visit = {
                'entered_at': date_format(entering_time, "d F Y \\г. \\в H:i"),
                'duration': formatted_duration,
                'is_strange': long_visit
            }
        this_passcard_visits.append(specific_visit)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
