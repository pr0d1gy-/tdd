from datetime import datetime, timedelta

from django.test import TestCase
from django.db import IntegrityError, transaction


class BaseTestCase(TestCase):

    def setUp(self):
        self.now = datetime.now()
        self.expire_date = self.now + timedelta(days=50)

    def _get_expire_date(self):
        return self.expire_date.month, self.expire_date.year


class BaseCardTestCase(BaseTestCase):

    def setUp(self):
        super(BaseCardTestCase, self).setUp()
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

        with transaction.atomic():
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
        from card.services import CardService, CardServiceException
        self.service = CardService
        self.service_exception = CardServiceException


class CheckCardServiceMethodsTestCase(BaseCardServiceTestCase):

    def test_create_method_exist(self):
        self.assertTrue(hasattr(self.service, 'create'))
        self.assertTrue(callable(getattr(self.service, 'create')))

    def test_remove_method_exist(self):
        self.assertTrue(hasattr(self.service, 'remove'))
        self.assertTrue(callable(getattr(self.service, 'remove')))


class ServiceCreateTestCase(BaseCardServiceTestCase):

    def test_wrong_number(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.create(None, None, None, None)
        e = cm.exception
        self.assertEqual(str(e), '`Number` is required.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('test', *self._get_expire_date(), 'Test Name')
        e = cm.exception
        self.assertEqual(str(e), '`Number` must have only numbers.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111', *self._get_expire_date(), 'Test Name')
        e = cm.exception
        self.assertEqual(str(e), '`Number` must have 16 digits.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('11112222333344445', *self._get_expire_date(),
                                'Test Name')
        e = cm.exception
        self.assertEqual(str(e), '`Number` must have 16 digits.')

    def test_wrong_month(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', None,
                                self.expire_date.year, 'Test')
        e = cm.exception
        self.assertEqual(str(e), '`Month` is required.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', 'test',
                                self.expire_date.year, 'Test')
        e = cm.exception
        self.assertEqual(str(e), '`Month` must have only numbers.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', '123',
                                self.expire_date.year, 'Test')
        e = cm.exception
        self.assertEqual(str(e), '`Month` should be in the range 1-12.')

    def test_wrong_year(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', self.expire_date.month,
                                None, 'Test')
        e = cm.exception
        self.assertEqual(str(e), '`Year` is required.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', self.expire_date.month,
                                'test', 'Test')
        e = cm.exception
        self.assertEqual(str(e), '`Year` must have only numbers.')

        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', self.expire_date.month,
                                (self.now.year - 2000) - 5, None)
        e = cm.exception
        self.assertEqual(str(e), '`Year` should be in the '
                                 'range {}-99.'.format(
            (self.now.year - 2000)
        ))

    def test_wrong_name(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', *self._get_expire_date(),
                                None)
        e = cm.exception
        self.assertEqual(str(e), '`Name` is required.')

    def test_unique(self):
        self.service.create('1111222233334444', self.expire_date.month,
                            self.expire_date.year, 'Test Name')
        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', self.expire_date.month,
                                self.expire_date.year, 'Test Name')
        e = cm.exception
        self.assertEqual(str(e), 'Card with such number already exists.')

    def test_validation_date(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.create('1111222233334444', self.now.month-1,
                                self.now.year, 'Test Name')

        e = cm.exception
        self.assertEqual(str(e), 'Expire date must be greater than current.')

    def test_create(self):
        self.service.create('1111222233334444', *self._get_expire_date(),
                            'Test Name')
        self.assertEqual(1, self.model.objects.all().count())


class ServiceDeleteTestCase(BaseCardServiceTestCase):

    def test_remove_not_exists(self):
        with self.assertRaises(self.service_exception) as cm:
            self.service.remove('1111222233334444')
        e = cm.exception
        self.assertEqual(str(e), 'Card with such name was not exists.')

    def test_remove(self):
        card = self.model(
            number='1111222233334444',
            month='01',
            year='19',
            name='Test Name'
        )
        card.save()

        self.assertEqual(1, self.model.objects.all().count())
        self.service.remove('1111222233334444')
        self.assertEqual(0, self.model.objects.all().count())
