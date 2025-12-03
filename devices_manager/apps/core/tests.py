"""
Tests for core models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core.models import BaseModel


class BaseModelTest(TestCase):
    """
    Test BaseModel abstract model.
    """

    def test_base_model_is_abstract(self):
        """
        Test that BaseModel is abstract.
        """
        self.assertTrue(BaseModel._meta.abstract)

