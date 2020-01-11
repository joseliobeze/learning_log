from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """Um assunto sobre o qual o usuário esta aprendendo."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Entry(models.Model):
    """Algo especificoaprendido sobre um assunto."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Metal:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Devolve uma representação em string do modelo."""
        return self.text if len(self.text) < 50 else f'{self.text[:50]}...'
