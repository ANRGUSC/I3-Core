from mixer.backend.django import mixer
import pytest

class TestModels:
    def test_is_seller(self):
        user = mixer.blend('accounts.User' , )
