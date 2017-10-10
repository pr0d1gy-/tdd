from django.test import TestCase
from django.db import IntegrityError


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


class CheckBaseModelFunctions(BaseCardTestCase):

    def test_saving_card(self):
        card = self.model(
            number='1111222233334444',
            month='01',
            year='19',
            name='Test Name'
        )
        card.save()

        loaded_card = self.model.objects.get(number=card.number)
        self.assertEqual(card, loaded_card)
        self.assertEqual(card.number, loaded_card.number)
        self.assertEqual(int(card.month), loaded_card.month)
        self.assertEqual(int(card.year), loaded_card.year)
        self.assertEqual(card.name, loaded_card.name)

    def test_saving_only_unique_card(self):
        card = self.model(
            number='1111222233334444',
            month='01',
            year='19',
            name='Test Name'
        )
        card.save()

        with self.assertRaises(IntegrityError):
            card2 = self.model(
                number='1111222233334444',
                month='02',
                year='20',
                name='Test Name2'
            )
            card2.save()

        card3 = self.model(
            number='1111222233335555',
            month='01',
            year='19',
            name='Test Name'
        )
        card3.save()

        self.assertEqual(2, self.model.objects.all().count())


class BaseCardServiceTestCase(BaseCardTestCase):

    def setUp(self):
        super(BaseCardServiceTestCase, self).setUp()
        from card.services import CardService
        self.service = CardService
