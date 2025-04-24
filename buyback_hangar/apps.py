from django.apps import AppConfig

class BuyBackHangarConfig(AppConfig):
    name = 'buyback_hangar'
    label = 'buyback_hangar'
    verbose_name = 'BuyBack Hangar'

    def ready(self):
        from . import signals  # future: to link setup or model signals
