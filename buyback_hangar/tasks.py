from celery import shared_task
from esi.decorators import token_required
from esi.clients import EsiClientProvider
from allianceauth.services.hooks import get_token
from django.utils.timezone import now
from .models import CorpHangarCache
from django.contrib.auth import get_user_model

User = get_user_model()
esi = EsiClientProvider()

@shared_task
def update_corp_hangar():
    for user in User.objects.filter(profile__main_character__isnull=False):
        character = user.profile.main_character
        token = get_token(character, 'esi-assets.read_corporation_hangars.v1')
        if not token or not token.valid:
            continue
        try:
            # Use django-esi to make the API call
            response = esi.client.Assets.get_corporations_corporation_id_assets(
                corporation_id=character.corporation_id,
                token=token.valid_access_token()
            )

            # Save the response data to the database
            CorpHangarCache.objects.update_or_create(
                character=character,
                defaults={
                    'json_data': response.result(),  # Use `.result()` to get the JSON response
                    'last_fetched': now()
                }
            )
        except Exception as e:
            print(f"Error fetching assets for {character}: {e}")
