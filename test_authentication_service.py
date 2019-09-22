import pytest
from authentication_service import AuthenticationService

@pytest.fixture('module')
def auth_service():
    return AuthenticationService()

def test_is_valid(auth_service):
    pass
