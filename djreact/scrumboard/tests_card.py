from django.test import TestCase
from django.core.validators import ValidationError

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

class CardValidations(TestCase):

    def test_card_title_is_required(self):
        test_object = Card(
            title=None,
            description='The description',
            list=List.objects.create(name="Test list"),
            story_points=3,
            businessValue=34,
        )

        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be null.']}"):
            test_object.full_clean()

    def test_card_title_cannot_be_blank(self):
        test_object = Card(
            title='',
            description='The description',
            list=List.objects.create(name="Test list"),
            story_points=3,
            businessValue=34,
        )

        with self.assertRaisesMessage(ValidationError, "{'title': ['This field cannot be blank.']}"):
            test_object.full_clean()

    def test_card_story_points_cannot_be_negative(self):
        test_object = Card(
            title='Some title',
            description='The description',
            list=List.objects.create(name="Test list"),
            story_points=-1,
            businessValue=34,
        )

        with self.assertRaisesMessage(ValidationError, "{'story_points': ['Ensure this value is greater than or equal to 0.']}"):
            test_object.full_clean()
                
    def test_card_businessValue_cannot_be_negative(self):
        test_object = Card(
            title='Some title',
            description='The description',
            list=List.objects.create(name="Test list"),
            story_points=34,
            businessValue=-1,
        )

        with self.assertRaisesMessage(ValidationError, "{'businessValue': ['Ensure this value is greater than or equal to 0.']}"):
            test_object.full_clean()

    def test_card_can_show_multiple_errors(self):
        error_message = "{'title': ['This field cannot be blank.'], "\
            "'list': ['This field cannot be null.'], "\
            "'story_points': ['Ensure this value is greater than or equal to 0.'], "\
            "'businessValue': ['Ensure this value is greater than or equal to 0.']}"
        test_object = Card(
            story_points=-1,
            businessValue=-1
        )
        
        with self.assertRaisesMessage(ValidationError, error_message):
            test_object.full_clean()