from celery import shared_task
from esi.clients import EsiClientProvider
from esi.models import Token
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
            # Retrieve the token for the character
            token = Token.objects.filter(character_id=character.character_id).first()
            if not token:
                print(f"No token found for {character}. Skipping.")
                continue

            # Refresh the token if it is expired
            if token.expires <= now():
                try:
                    token = token.refresh()
                except Exception as e:
                    print(f"Failed to refresh token for {character}: {e}")
                    continue

            # Fetch the roles for the character
            response = esi.client.Corporation.get_corporations_corporation_id_roles(
                corporation_id=character.corporation_id,
                token=token.access_token
            )
            roles = [role['role'] for role in response.result()]  # Extract roles

            # Check if the character has the 'Director' role
            if 'Director' not in roles:
                continue  # Skip non-directors

            # Fetch hangar assets
            response = esi.client.Assets.get_corporations_corporation_id_assets(
                corporation_id=character.corporation_id,
                token=token.access_token
            )
            assets = response.result()  # Extract JSON response

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
