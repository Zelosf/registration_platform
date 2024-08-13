from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse ,HttpResponseForbidden
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from rest_framework.exceptions import ValidationError


# Retrieving all required data about the program
@login_required
def program_list(request):
    # Retrieving program data.
    response_programs = requests.get(f'{settings.APP_A_URL}/api/programs/')
    programs = response_programs.json() if response_programs.status_code == 200 else []
    # Retrieving event name by event ID.
    response_events = requests.get(f'{settings.APP_A_URL}/api/events/')
    events = response_events.json() if response_events.status_code == 200 else {}
    event_names = {event['id']: event['name'] for event in events}
    # Retrieving Speaker name by Speaker ID.
    response_speakers = requests.get(f'{settings.APP_A_URL}/api/speakers/')
    speakers = response_speakers.json() if response_speakers.status_code == 200 else {}
    speaker_name = {speaker['id']: speaker['name'] for speaker in speakers}
    for program in programs:
        program['event_name'] = event_names.get(program['event'], 'Unknown Event')
        program['speaker_name'] = speaker_name.get(program['speaker'], 'Unknown Speaker')

    context = {
        'programs': programs,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'events/programs.html', context)


# Retrieving full information about the Speaker
def speaker_detail(request, speaker_id):
    response = requests.get(f'{settings.APP_A_URL}/api/speakers/{speaker_id}/')
    speaker = response.json()
    return render(request, 'events/speaker_detail.html', {'speaker': speaker})


# Registers a user via the ticket creation API.
@login_required
@require_POST
def register(request):
    try:
        data = json.loads(request.body)

        # Sending data to an external API
        response = requests.post(f'{settings.APP_A_URL}/api/tickets/', json=data)

        # Returning response from the external API
        return JsonResponse({"success": True})
    except ValidationError as e:
        return JsonResponse({"success": False, "message": str(e)})
    except Exception as e:
        return JsonResponse({"success": False, "message": "An unexpected error occurred."})


# Retrieves all required fields, including values for the drop-down menu
@login_required
def edit_program(request, program_id):
    # Checking for superuser status
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit programs.")

    response = requests.get(f'{settings.APP_A_URL}/api/programs/{program_id}/')
    if response.status_code != 200:
        return redirect('/program/')

    program = response.json()
    events_response = requests.get(f'{settings.APP_A_URL}/api/events/')
    speakers_response = requests.get(f'{settings.APP_A_URL}/api/speakers/')

    if events_response.status_code == 200:
        events = events_response.json()
    else:
        events = []

    if speakers_response.status_code == 200:
        speakers = speakers_response.json()
    else:
        speakers = []

    if request.method == 'POST':
        data = {
            'event': request.POST['event_name'],
            'date': request.POST['date'],
            'start_time': request.POST['start_time'],
            'end_time': request.POST['end_time'],
            'description': request.POST['description'],
            'available_tickets': request.POST['available_tickets'],
            'total_tickets': request.POST['total_tickets'],
            'speaker': request.POST['speaker']
        }
        update_response = requests.put(
            f'{settings.APP_A_URL}/api/programs/{program_id}/',
            json=data
        )
        if update_response.status_code == 200:
            return redirect('/program/')
        else:
            return render(request, 'events/edit_program.html',
                          {'program': program, 'events': events, 'speakers': speakers,
                           'error': 'Failed to update program.'})

    return render(request, 'events/edit_program.html', {'program': program, 'events': events, 'speakers': speakers})


@login_required
def user_tickets(request):
    # Retrieving the list of tickets for the current user
    response_tickets = requests.get(f'{settings.APP_A_URL}/api/tickets/', params={'user': request.user.id})
    tickets = response_tickets.json() if response_tickets.status_code == 200 else []

    # Retrieving data about programs
    response_programs = requests.get(f'{settings.APP_A_URL}/api/programs/')
    programs = response_programs.json() if response_programs.status_code == 200 else []
    programs_date = {program['id']: program['date'] for program in programs}
    programs_start_time = {program['id']: program['start_time'] for program in programs}
    programs_end_time = {program['id']: program['end_time'] for program in programs}
    programs_event = {program['id']: program['event'] for program in programs}
    programs_speaker = {program['id']: program['speaker'] for program in programs}

    # Retrieving data about events
    response_events = requests.get(f'{settings.APP_A_URL}/api/events/')
    events = response_events.json() if response_events.status_code == 200 else {}
    event_names = {event['id']: event['name'] for event in events}

    # Retrieving data about speakers
    response_speakers = requests.get(f'{settings.APP_A_URL}/api/speakers/')
    speakers = response_speakers.json() if response_speakers.status_code == 200 else {}
    speaker_name = {speaker['id']: speaker['name'] for speaker in speakers}

    # Updating ticket information
    for ticket in tickets:
        program_id = ticket.get('program')
        ticket['programs_date'] = programs_date.get(program_id, 'Unknown Date')
        ticket['programs_start_time'] = programs_start_time.get(program_id, 'Unknown Start Time')
        ticket['programs_end_time'] = programs_end_time.get(program_id, 'Unknown End Time')
        ticket['programs_event'] = programs_event.get(program_id, 'Unknown Event ID')
        ticket['program_event_name'] = event_names.get(programs_event.get(program_id), 'Unknown Event')
        ticket['programs_speaker'] = programs_speaker.get(program_id, 'Unknown Speaker ID')
        ticket['program_speaker_name'] = speaker_name.get(programs_speaker.get(program_id), 'Unknown Speaker')

    return render(request, 'events/user_tickets.html', {'tickets': tickets})