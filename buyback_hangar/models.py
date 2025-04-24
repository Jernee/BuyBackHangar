from django.db import models
from allianceauth.eveonline.models import EveCharacter

class CorpHangarCache(models.Model):
    character = models.OneToOneField(EveCharacter, on_delete=models.CASCADE)
    last_fetched = models.DateTimeField(auto_now=True)
    json_data = models.JSONField()


from django.db import models

class TrackedHangarLocation(models.Model):
    location_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.location_id})"
