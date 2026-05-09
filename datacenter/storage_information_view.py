from datacenter.models import Visit
from datacenter.models import format_duration
from django.shortcuts import render
from django.utils.formats import date_format
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []
    current_visitors = Visit.objects.filter(leaved_at__isnull=True)
    for visitor in current_visitors:
        name = visitor.passcard
        entering_time = localtime(value=visitor.entered_at, timezone=None)
        delta_total_seconds = visitor.get_duration()
        formatted_duration = format_duration(delta_total_seconds)
        visit_card = {
            'who_entered': name,
            'entered_at': date_format(entering_time, "d F Y \\г. \\в H:i"),
            'duration': formatted_duration,
        }
        non_closed_visits.append(visit_card)

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
