from django.db import transaction
from .models import ParsedEmail, ParsedUrl


@transaction.atomic
def save_new_emails(url: str, emails: list) -> None:
    emails_objects = [ParsedEmail.objects.get_or_create(email=e)[0] for e in emails]
    url_object, _ = ParsedUrl.objects.get_or_create(url=url)
    url_object.emails.add(*emails_objects)
    url_object.save()


def get_url_list(email: str) -> list:
    return [obj.url for obj in ParsedUrl.objects.filter(emails__email=email)]
