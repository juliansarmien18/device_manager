"""
Tests for core models.
"""

from apps.core.models import BaseModel
from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseModelTest(TestCase):
    """
    Test BaseModel abstract model.
    """

    def test_base_model_is_abstract(self):
        """
        Test that BaseModel is abstract.
        """
        self.assertTrue(BaseModel._meta.abstract)
