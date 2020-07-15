from django.test import TestCase

from .models import List
from .serializers import ListSerializer


class ListTests(TestCase):
    test_name = 'The List'

    def setUp(self):
        List.objects.create(name=self.test_name)

    def test_list_keeps_name(self):
        test_object = List.objects.get(name=self.test_name)

        assert test_object.name == self.test_name

    def test_list_displays_nicely(self):
        test_object = List.objects.get(name=self.test_name)

        assert f'{test_object}' == f'List: {self.test_name}'

    def test_list_serializes_properly(self):
        test_object = List.objects.get(name=self.test_name)
        serialized = ListSerializer(test_object)

        assert serialized.data == {'id': test_object.id, 'name': self.test_name}
