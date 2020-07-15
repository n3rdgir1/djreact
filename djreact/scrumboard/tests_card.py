from django.test import TestCase

from .models import Card, List
from .serializers import CardSerializer

class CardTests(TestCase):

    test_title = 'The Card'
    test_description = 'the description that has a lot of words'

    def setUp(self):
        list = List.objects.create(name="Test list")
        Card.objects.create(
            title=self.test_title,
            description=self.test_description,
            list=list,
            story_points=3,
            businessValue=34
        )

    def test_card_keeps_attributes(self):
        test_object = Card.objects.get(title=self.test_title)
        assert test_object.title == self.test_title
        assert test_object.description == self.test_description
        assert test_object.list == List.objects.get(name="Test list")
        assert test_object.story_points == 3
        assert test_object.businessValue == 34

    def test_card_displays_nicely(self):
        test_object = Card.objects.get(title=self.test_title)
        assert f'{test_object}' == f'Card: {self.test_title}'

    def test_card_serializes_correctly(self):
        test_object = Card.objects.get(title=self.test_title)
        serialized = CardSerializer(test_object)

        assert serialized.data == {
                                    'id': test_object.id, 
                                    'title': self.test_title,
                                    'description': self.test_description,
                                    'list': List.objects.get(name="Test list").id,
                                    'story_points': 3,
                                    'businessValue': 34
                                  }
