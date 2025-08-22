from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='accounts',
        verbose_name="Usuário"
    )
    name = models.CharField("Nome", max_length=50)

    class Meta:
        unique_together = [('owner', 'name')]
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return f"{self.name} ({self.owner.username})"


class Category(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='categories',
        verbose_name="Usuário"
    )
    name = models.CharField("Nome", max_length=50)

    class Meta:
        unique_together = [('owner', 'name')]
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME, EXPENSE = 'IN', 'OUT'
    KIND_CHOICES = [(INCOME, 'Renda'), (EXPENSE, 'Despesa')]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transactions',
        verbose_name="Usuário"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='transactions',
        verbose_name="Conta"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Categoria"
    )
    kind = models.CharField("Tipo", max_length=3, choices=KIND_CHOICES)
    amount = models.DecimalField("Valor", max_digits=12, decimal_places=2)
    date = models.DateField("Data")
    description = models.CharField("Descrição", max_length=200, blank=True)

    class Meta:
        ordering = ['-date', '-id']
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def sign_amount(self):
        return self.amount if self.kind == self.INCOME else -self.amount
