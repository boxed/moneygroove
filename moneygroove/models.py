from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    IntegerField,
    Model,
)


class User(AbstractUser):
    target_savings = IntegerField(default=0)


class ExpectedIncome(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    name = CharField(max_length=255)
    amount = IntegerField()
    expected_date = IntegerField(null=True)

    class Meta:
        ordering = ('pk',)


class ExpectedExpense(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    name = CharField(max_length=255)
    amount = IntegerField()
    expected_date = IntegerField(null=True)

    class Meta:
        ordering = ('pk',)
