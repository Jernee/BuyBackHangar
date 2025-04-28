from celery import shared_task
from allianceauth.services.hooks.esi import esi_client
from allianceauth.services.hooks import get_token
from django.utils.timezone import now
from .models import CorpHangarCache
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def update_corp_hangar():
    for user in User.objects.filter(profile__main_character__isnull=False):
        character = user.profile.main_character
        token = get_token(character, 'esi-assets.read_corporation_hangars.v1')
        if not token or not token.valid:
            continue
        try:
            client = esi_client()
            response = client.Assets.get_corporations_corporation_id_assets(
                corporation_id=character.corporation_id,
                token=token.valid_access_token()
            )
            CorpHangarCache.objects.update_or_create(
                character=character,
                defaults={
                    'json_data': response.result(),
                    'last_fetched': now()
                }
            )
        except Exception as e:
            print(f"Error fetching assets for {character}: {e}")
