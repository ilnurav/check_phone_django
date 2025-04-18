from django.db import models

class PhoneRange(models.Model):
    abc = models.CharField(max_length=3, verbose_name="Код DEF/ABC")
    start = models.BigIntegerField(verbose_name="Начало диапазона")
    end = models.BigIntegerField(verbose_name="Конец диапазона")
    capacity = models.IntegerField(verbose_name="Емкость")
    operator = models.CharField(max_length=255, verbose_name="Оператор")
    region = models.CharField(max_length=255, verbose_name="Регион")
    territory_gar = models.CharField(max_length=255, verbose_name="Территория ГАР")
    inn = models.CharField(max_length=12, verbose_name="ИНН")

    class Meta:
        indexes = [
            models.Index(fields=['abc', 'start', 'end']),
        ]
        verbose_name = "Диапазон номеров"
        verbose_name_plural = "Диапазоны номеров"

    def __str__(self):
        return f"{self.abc}: {self.start}-{self.end} ({self.operator})"