from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CorpHangarCache, TrackedHangarLocation

@login_required
def corp_hangar(request):
    character = request.user.profile.main_character
    try:
        cache = CorpHangarCache.objects.get(character=character)
        assets = cache.json_data
        location_ids = list(TrackedHangarLocation.objects.filter(enabled=True).values_list('location_id', flat=True))
        if location_ids:
            assets = [item for item in assets if item['location_id'] in location_ids]
        return render(request, 'buyback_hangar/hangar.html', {
            'assets': assets,
            'character': character
        })
    except CorpHangarCache.DoesNotExist:
        return render(request, 'buyback_hangar/hangar.html', {
            'error': 'No cached data found. Try again later.'
        })
