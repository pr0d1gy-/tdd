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
    def create(number, month, year, name):
        pass

    @staticmethod
    def remove(number):
        try:
            card = Card.objects.get(number=number)
        except Card.DoesNotExist:
            raise CardServiceException('Card with such name was not exists.')
        else:
            card.delete()
        return True
