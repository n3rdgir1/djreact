from django.test import TestCase

from .models import List
from .serializers import ListSerializer


class ListTests(TestCase):
    test_name = 'The List'

    def setUp(self):
        List.objects.create(name=self.test_name)

    @property
    def test_object(self):
        return List.objects.get(name=self.test_name)

    def test_list_keeps_name(self):
        assert self.test_object.name == self.test_name

    def test_list_displays_nicely(self):
        assert f'{self.test_object}' == f'List: {self.test_name}'

    def test_list_serializes_properly(self):
        serialized = ListSerializer(self.test_object)

        assert serialized.data == {'id': self.test_object.id, 'name': self.test_name}
