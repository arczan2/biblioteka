from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    description = models.CharField(max_length=120, default='brak opisu')

    def clean(self):
        from django.core.exceptions import ValidationError
        # Jeżeli nazwa książki jest pusta to zwróć wyjątek
        if self.name is None or self.name == '':
            raise ValidationError('Nazwa książki nie moze być pusta')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
