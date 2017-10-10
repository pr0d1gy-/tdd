from django.test import TestCase


class BaseCardTestCase(TestCase):

    def setUp(self):
        from card.models import Card
        self.model = Card
