from django.test import TestCase


class BaseTestCase(TestCase):
    """
    To jest test do sprawdznia działania github actions
    Po dodaniu prawdziwych testów może zostać usunięta
    """

    def test_base(self):
        self.assertEqual(True, True)
