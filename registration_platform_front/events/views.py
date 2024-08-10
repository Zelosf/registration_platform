from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import requests


def program_list(request):
    response_programs = requests.get('http://localhost:8000/api/programs/')
    programs = response_programs.json() if response_programs.status_code == 200 else []

    response_events = requests.get('http://localhost:8000/api/events/')
    events = response_events.json() if response_events.status_code == 200 else {}
    event_names = {event['id']: event['name'] for event in events}
    event_dates = {event['id']: event['date'] for event in events}

    response_speakers = requests.get('http://localhost:8000/api/speakers/')
    speakers = response_speakers.json() if response_speakers.status_code == 200 else {}
    speaker_name = {speaker['id']: speaker['name'] for speaker in speakers}
    for program in programs:
        program['event_name'] = event_names.get(program['event'], 'Unknown Event')
        program['event_date'] = event_dates.get(program['event'], 'Unknown Event')
        program['speaker_name'] = speaker_name.get(program['speaker'], 'Unknown Speaker')

    return render(request, 'events/programs.html', {'programs': programs})


def event_list(request):
    response = requests.get('http://localhost:8000/api/events/')
    events = response.json()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, event_id):
    response = requests.get(f'http://localhost:8000/api/events/{event_id}/')
    event = response.json()
    return render(request, 'events/event_detail.html', {'event': event})


def speaker_detail(request, speaker_id):
    response = requests.get(f'http://localhost:8000/api/speakers/{speaker_id}/')
    speaker = response.json()
    return render(request, 'events/speaker_detail.html', {'speaker': speaker})


def register(request):
    if request.method == 'POST':
        data = request.POST
        response = requests.post('http://localhost:8000/api/tickets/', json=data)
        return JsonResponse(response.json())
