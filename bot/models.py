from django.db import models


class BotUser(models.Model):
    tg_id = models.PositiveBigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.phone)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
