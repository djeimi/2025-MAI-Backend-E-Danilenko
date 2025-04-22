from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pattern
import requests
from crochetProject import settings

@receiver(post_save, sender=Pattern)
def send_update_to_centrifugo(sender, instance, created, **kwargs):
    if created:
        data = {
            "channel": instance.author.username,
            "data": {
                "title": instance.title,
                "description": instance.description,
                "id": instance.id
            }
        }

        url = "http://centrifugo:3000/api/publish"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key":  settings.CENTRIFUGO_API_KEY
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")