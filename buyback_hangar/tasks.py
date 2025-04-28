from celery import shared_task
from esi.clients import EsiClientProvider
from esi.decorators import token_required
from django.utils.timezone import now
from .models import CorpHangarCache
from django.contrib.auth import get_user_model

User = get_user_model()
esi = EsiClientProvider()

@shared_task
def update_corp_hangar():
    for user in User.objects.filter(profile__main_character__isnull=False):
        character = user.profile.main_character

        try:
            # Fetch the roles for the character
            @token_required('esi-corporations.read_corporation_roles.v1')
            def fetch_roles(token):
                response = esi.client.Corporation.get_corporations_corporation_id_roles(
                    corporation_id=character.corporation_id,
                    token=token.valid_access_token()
                )
                return [role['role'] for role in response.result()]  # Extract roles

            roles = fetch_roles(character)

            # Check if the character has the 'Director' role
            if 'Director' not in roles:
                continue  # Skip non-directors

            # Fetch hangar assets
            @token_required('esi-assets.read_corporation_hangars.v1')
            def fetch_hangar_assets(token):
                response = esi.client.Assets.get_corporations_corporation_id_assets(
                    corporation_id=character.corporation_id,
                    token=token.valid_access_token()
                )
                return response.result()  # Extract JSON response

            assets = fetch_hangar_assets(character)

            # Save the response data to the database
            CorpHangarCache.objects.update_or_create(
                character=character,
                defaults={
                    'json_data': assets,
                    'last_fetched': now()
                }
            )
        except Exception as e:
            print(f"Error fetching assets for {character}: {e}")
