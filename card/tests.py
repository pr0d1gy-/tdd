from django.test import TestCase


class BaseCardTestCase(TestCase):

    def setUp(self):
        from card.models import Card
        self.model = Card


class CheckCardFieldsTestCase(BaseCardTestCase):

    def test_card_number_field(self):
        self.assertTrue(hasattr(self.model, 'number'))

    def test_card_month_field(self):
        self.assertTrue(hasattr(self.model, 'month'))

    def test_card_year_field(self):
        self.assertTrue(hasattr(self.model, 'year'))

    def test_card_name_field(self):
        self.assertTrue(hasattr(self.model, 'name'))


class BaseCardServiceTestCase(BaseCardTestCase):

    def setUp(self):
        super(BaseCardServiceTestCase, self).setUp()
        from card.services import CardService
        self.service = CardService
