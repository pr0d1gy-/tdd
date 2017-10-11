from datetime import datetime

from django.db import IntegrityError

from card.models import Card


class CardServiceException(Exception):
    pass


class CardService(object):

    @staticmethod
    def check_for_existing(number, is_raise_exception=True):
        try:
            Card.objects.get(number=number)
        except Card.DoesNotExist:
            return True
        else:
            if is_raise_exception:
                raise CardServiceException(
                    'Card with such number already exists.')
            return False

    @staticmethod
    def validate_number(number):
        if not number:
            raise CardServiceException('`Number` is required.')

        try:
            number = int(number)
        except ValueError:
            raise CardServiceException('`Number` must have only numbers.')

        if len(str(number)) != 16:
            raise CardServiceException('`Number` must have 16 digits.')

        return number

    @staticmethod
    def validate_month(month):
        if not month:
            raise CardServiceException('`Month` is required.')

        try:
            month = int(month)
        except ValueError:
            raise CardServiceException('`Month` must have only numbers.')

        if not 1 <= month <= 12:
            raise CardServiceException('`Month` should be in the range 1-12.')

        return month

    @staticmethod
    def validate_year(year):
        if not year:
            raise CardServiceException('`Year` is required.')

        try:
            year = int(year)
        except ValueError:
            raise CardServiceException('`Year` must have only numbers.')

        now_year = datetime.now().year
        if year < (now_year - 2000):
            raise CardServiceException(
                '`Year` should be in the range {}-99.'.format(
                    now_year - 2000))

        return year

    @staticmethod
    def validate_name(name):
        if not name:
            raise CardServiceException('`Name` is required.')

        return name

    @staticmethod
    def validate_date(month, year):
        now = datetime.now()
        if year > now.year:
            return True
        if month >= now.month and \
                year == now.year:
            return True
        raise CardServiceException(
            'Expire date must be greater than current.')

    @staticmethod
    def create(number, month, year, name):
        number = CardService.validate_number(number)
        month = CardService.validate_month(month)
        year = CardService.validate_year(year)
        name = CardService.validate_name(name)

        CardService.validate_date(month, year)
        CardService.check_for_existing(number)

        card = Card(
            number=number,
            month=month,
            year=year,
            name=name
        )

        try:
            card.save()
        except IntegrityError:
            raise CardServiceException('Card with such number already exists.')

        return card

    @staticmethod
    def remove(number):
        try:
            card = Card.objects.get(number=number)
        except Card.DoesNotExist:
            raise CardServiceException('Card with such name was not exists.')
        else:
            card.delete()
        return True
