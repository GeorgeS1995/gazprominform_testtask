import os
import pytest
from django.conf import settings
from rest_framework import status
from .conftest import get_json_testdata


class TestEmailApiView:
    path_to_service = "/services/service2"

    @pytest.mark.parametrize("t_data", [
        ("", {'detail': "Get parameter 'email' wasn't passed"}),
        ("wrong_email", {'detail': "wrong_email is not a valid email"}),
    ])
    def test_not_valid_email(self, client, token, t_data):
        r = client.get(self.path_to_service, {**token, "email": t_data[0]})
        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert r.data == t_data[1]

    @pytest.mark.django_db
    @pytest.mark.parametrize("t_data", get_json_testdata(
        os.path.join(settings.BASE_DIR, "gazprominfo_app", "test", "test_data", "test_success_get_emails.json")))
    def test_success_get_emails(self, fill_db, t_data, client, token):
        r = client.get(self.path_to_service, {**token, "email": t_data['email']})
        assert r.status_code == status.HTTP_200_OK
        assert r.data == t_data
