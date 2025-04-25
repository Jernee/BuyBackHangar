from django.dispatch import receiver
from allianceauth.authentication.signals import user_created
import logging

logger = logging.getLogger(__name__)

@receiver(user_created)
def handle_new_user(sender, user, **kwargs):
    logger.info(f"[BuyBackHangar] New user created: {user.username}")
