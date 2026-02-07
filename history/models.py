from django.db import models
from django.contrib.auth.models import User

class GenerationHistory(models.Model):
    DATA_TYPE_CHOICES = [
        ('person', 'Pessoa'),
        ('company', 'Empresa'),
        ('pokemon', 'Pokémon'),
        ('dog', 'Cachorro'),
    ]

    EXPORT_FORMAT_CHOICES = [
        ('preview', 'Visualização'),
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generations')
    data_type = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    export_format = models.CharField(max_length=10, choices=EXPORT_FORMAT_CHOICES, default='preview')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Histórico de Geração'
        verbose_name_plural = 'Histórico de Gerações'

    def __str__(self):
        return f"{self.user.username} - {self.get_data_type_display()} ({self.quantity}) em {self.created_at.strftime('%d/%m/%Y %H:%M')}"
