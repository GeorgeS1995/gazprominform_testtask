import json
import pytest
from django.conf import settings
from ..models import ParsedUrl, ParsedEmail


def get_json_testdata(path_to_cases: str) -> list:
    with open(path_to_cases) as f:
        return json.load(f)


@pytest.fixture
def token():
    """ Returns a valid token for testcases """
    return {'token': settings.GETPARAMETER_TOKEN}


@pytest.fixture
def fill_db(db):
    for e in ['gazprom@gazprom.ru', 'example@example.com', 'empty@example.com']:
        email_obj = ParsedEmail.objects.create(email=e)
        email_obj.save()

    for url in ['https://www.gazprom.ru/contacts/', 'https://example.ru']:
        obj = ParsedUrl.objects.create(url=url)
        obj.emails.add(ParsedEmail.objects.get(email="example@example.com"))
        if url == 'https://www.gazprom.ru/contacts/':
            obj.emails.add(ParsedEmail.objects.get(email="gazprom@gazprom.ru"))
        obj.save()

    yield

    for url_obj in ParsedUrl.objects.all():
        url_obj.emails.clear()
        url_obj.delete()

    for email_obj in ParsedEmail.objects.all():
        email_obj.delete()
