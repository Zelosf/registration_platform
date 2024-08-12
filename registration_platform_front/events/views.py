from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

from rest_framework.exceptions import ValidationError


@login_required
def program_list(request):
    response_programs = requests.get(f'{settings.APP_A_URL}/api/programs/')
    programs = response_programs.json() if response_programs.status_code == 200 else []

    response_events = requests.get(f'{settings.APP_A_URL}/api/events/')
    events = response_events.json() if response_events.status_code == 200 else {}
    event_names = {event['id']: event['name'] for event in events}
    event_dates = {event['id']: event['date'] for event in events}

    response_speakers = requests.get(f'{settings.APP_A_URL}/api/speakers/')
    speakers = response_speakers.json() if response_speakers.status_code == 200 else {}
    speaker_name = {speaker['id']: speaker['name'] for speaker in speakers}
    for program in programs:
        program['event_name'] = event_names.get(program['event'], 'Unknown Event')
        program['event_date'] = event_dates.get(program['event'], 'Unknown Event')
        program['speaker_name'] = speaker_name.get(program['speaker'], 'Unknown Speaker')

    return render(request, 'events/programs.html', {'programs': programs})


def event_list(request):
    response = requests.get(f'{settings.APP_A_URL}/api/events/')
    events = response.json()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    response = requests.get(f'{settings.APP_A_URL}/api/events/{event_id}/')
    event = response.json()
    return render(request, 'events/event_detail.html', {'event': event})


def speaker_detail(request, speaker_id):
    response = requests.get(f'{settings.APP_A_URL}/api/speakers/{speaker_id}/')
    speaker = response.json()
    return render(request, 'events/speaker_detail.html', {'speaker': speaker})


@login_required
@require_POST
def register(request):
    try:
        # Получение данных из тела запроса
        data = json.loads(request.body)

        # Отправка данных на внешний API
        response = requests.post(f'{settings.APP_A_URL}/api/tickets/', json=data)

        # Возврат ответа от внешнего API
        return JsonResponse({"success": True})
    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)})
    except Exception as e:
        return JsonResponse({"success": False, "message": "An unexpected error occurred."})
