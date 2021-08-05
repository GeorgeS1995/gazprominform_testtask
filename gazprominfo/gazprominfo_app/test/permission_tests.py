import pytest
from rest_framework import status


@pytest.mark.parametrize("url", ['/services/service1', "/services/service2"])
@pytest.mark.parametrize("token_value", ['wrong_token', ''])
def test_permission_error(token_value, url, client):
    """ Tests wrong and empty token with all services """
    r = client.get(url, {"token": token_value})
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert r.data == {"detail": "Empty or wrong get parameter 'token'"}
