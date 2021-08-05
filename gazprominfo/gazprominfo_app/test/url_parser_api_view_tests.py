import os
import pytest
from requests import RequestException
from requests_html import HTMLSession
from rest_framework import status
from django.conf import settings
from .conftest import get_json_testdata
from .mock_objects import FakeReponse


class TestUrlParserApiView:
    path_to_service = "/services/service1"

    @pytest.mark.parametrize("t_data", [("not valid url", {'detail': "Url 'not valid url' is not valid."}),
                                        ("", {'detail': 'Empty url-to-parse get parameter'})])
    def test_invalide_url(self, t_data, client, token):
        r = client.get(self.path_to_service, {**token, "url-to-parse": t_data[0]})
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert r.data == t_data[1]

    def test_url_connection_error(self, client, token, monkeypatch):
        def _mocked_session_get(s, url):
            raise RequestException()

        monkeypatch.setattr(HTMLSession, "get", _mocked_session_get)

        r = client.get(self.path_to_service, {**token, "url-to-parse": "https://ya.ru"})
        assert r.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert r.data == {'detail': 'Resource https://ya.ru is not available or other connection error.'}

    @pytest.mark.parametrize("t_data", get_json_testdata(
        os.path.join(settings.BASE_DIR, "gazprominfo_app", "test", "test_data", "test_success_parse.json")))
    @pytest.mark.django_db
    def test_success_parse(self, client, token, monkeypatch, t_data):
        def _mocked_session_get(s, url):
            return FakeReponse(t_data['html'])

        monkeypatch.setattr(HTMLSession, "get", _mocked_session_get)
        r = client.get(self.path_to_service, {**token, "url-to-parse": "https://ya.ru"})
        assert r.status_code == status.HTTP_200_OK
        assert {'url': 'https://ya.ru', 'emails': t_data['emails']}
