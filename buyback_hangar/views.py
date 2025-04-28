from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from buyback_hangar.models import CorpHangarCache

@login_required
def corp_hangar(request):
    character = request.user.profile.main_character
    try:
        cache = CorpHangarCache.objects.get(character=character)
        assets = cache.json_data  # Extract the JSON data containing hangar items
    except CorpHangarCache.DoesNotExist:
        cache = None
        assets = []  # No assets if no cache exists

    return render(request, 'buyback_hangar/hangar.html', {
        'assets': assets,
        'character': character,
    })
