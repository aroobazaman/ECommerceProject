# shop/management/commands/clear_expired_tokens.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import UserToken

class Command(BaseCommand):
    help = 'Clear expired tokens'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        UserToken.objects.filter(expires_at__lt=now).delete()
        self.stdout.write('Expired tokens cleared.')
