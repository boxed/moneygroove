from pytest import approx
import time_machine
from iommi.struct import Struct

from moneygroove.models import ExpectedExpense
from moneygroove.views import (
    build_expected_lines,
    previous_month_length,
)


def test_build_expected_lines_30_days_previous_month():
    with time_machine.travel('2023-10-14'):
        assert previous_month_length() == 30

        expenses = [
            ExpectedExpense(amount=5_000, expected_date=30),
            ExpectedExpense(amount=3_000, expected_date=31),
        ]
        target_savings = 500
        lines = build_expected_lines(
            sum_income=10_000,
            sum_expenses=sum(x.amount for x in expenses),
            expenses=expenses,
            target_savings=target_savings,
        )
        per_day = 50
        assert lines[-2].benchmark - lines[-1].benchmark == approx(per_day, 0.1)
        assert lines[-1].benchmark - per_day == approx(target_savings, 0.01)

        assert lines == [
            Struct(benchmark=10000, date=25),
            Struct(benchmark=9950, date=26),
            Struct(benchmark=9900, date=27),
            Struct(benchmark=9850, date=28),
            Struct(benchmark=9800, date=29),
            Struct(benchmark=1750, date=30),  # big jump because both expenses end up on this day
            Struct(benchmark=1700, date=1),
            Struct(benchmark=1650, date=2),
            Struct(benchmark=1600, date=3),
            Struct(benchmark=1550, date=4),
            Struct(benchmark=1500, date=5),
            Struct(benchmark=1450, date=6),
            Struct(benchmark=1400, date=7),
            Struct(benchmark=1350, date=8),
            Struct(benchmark=1300, date=9),
            Struct(benchmark=1250, date=10),
            Struct(benchmark=1200, date=11),
            Struct(benchmark=1150, date=12),
            Struct(benchmark=1100, date=13),
            Struct(benchmark=1050, date=14),
            Struct(benchmark=1000, date=15),
            Struct(benchmark=950, date=16),
            Struct(benchmark=900, date=17),
            Struct(benchmark=850, date=18),
            Struct(benchmark=800, date=19),
            Struct(benchmark=750, date=20),
            Struct(benchmark=700, date=21),
            Struct(benchmark=650, date=22),
            Struct(benchmark=600, date=23),
            Struct(benchmark=550, date=24),
        ]


def test_build_expected_lines_31_days_previous_month():
    with time_machine.travel('2023-09-14'):
        assert previous_month_length() == 31

        expenses = [
            ExpectedExpense(amount=5_000, expected_date=30),
            ExpectedExpense(amount=3_000, expected_date=31),
        ]
        target_savings = 500
        lines = build_expected_lines(
            sum_income=10_000,
            sum_expenses=sum(x.amount for x in expenses),
            expenses=expenses,
            target_savings=target_savings,
        )
        per_day = 50
        assert lines[-2].benchmark - lines[-1].benchmark == approx(per_day, 0.1)
        # assert lines[-1].benchmark - per_day == approx(target_savings, 0.01)

        assert lines == [
            Struct(benchmark=10000, date=26),
            Struct(benchmark=9951, date=27),
            Struct(benchmark=9903, date=28),
            Struct(benchmark=9854, date=29),
            Struct(benchmark=4806, date=30),  # big jump, expense 1
            Struct(benchmark=1758, date=31),  # big jump, expense 2
            Struct(benchmark=1709, date=1),
            Struct(benchmark=1661, date=2),
            Struct(benchmark=1612, date=3),
            Struct(benchmark=1564, date=4),
            Struct(benchmark=1516, date=5),
            Struct(benchmark=1467, date=6),
            Struct(benchmark=1419, date=7),
            Struct(benchmark=1370, date=8),
            Struct(benchmark=1322, date=9),
            Struct(benchmark=1274, date=10),
            Struct(benchmark=1225, date=11),
            Struct(benchmark=1177, date=12),
            Struct(benchmark=1129, date=13),
            Struct(benchmark=1080, date=14),
            Struct(benchmark=1032, date=15),
            Struct(benchmark=983, date=16),
            Struct(benchmark=935, date=17),
            Struct(benchmark=887, date=18),
            Struct(benchmark=838, date=19),
            Struct(benchmark=790, date=20),
            Struct(benchmark=741, date=21),
            Struct(benchmark=693, date=22),
            Struct(benchmark=645, date=23),
            Struct(benchmark=596, date=24),
        ]


def test_build_expected_lines_31_days_previous_month__2():
    with time_machine.travel('2023-08-27'):
        assert previous_month_length() == 31

        expenses = [
            ExpectedExpense(amount=5_000, expected_date=30),
            ExpectedExpense(amount=3_000, expected_date=31),
        ]
        target_savings = 500
        lines = build_expected_lines(
            sum_income=10_000,
            sum_expenses=sum(x.amount for x in expenses),
            expenses=expenses,
            target_savings=target_savings,
        )
        per_day = 50
        assert lines[-2].benchmark - lines[-1].benchmark == approx(per_day, 0.1)
        # assert lines[-1].benchmark - per_day == approx(target_savings, 0.01)

        assert lines == [
            Struct(benchmark=10000, date=26),
            Struct(benchmark=9951, date=27),
            Struct(benchmark=9903, date=28),
            Struct(benchmark=9854, date=29),
            Struct(benchmark=4806, date=30),  # big jump, expense 1
            Struct(benchmark=1758, date=31),  # big jump, expense 2
            Struct(benchmark=1709, date=1),
            Struct(benchmark=1661, date=2),
            Struct(benchmark=1612, date=3),
            Struct(benchmark=1564, date=4),
            Struct(benchmark=1516, date=5),
            Struct(benchmark=1467, date=6),
            Struct(benchmark=1419, date=7),
            Struct(benchmark=1370, date=8),
            Struct(benchmark=1322, date=9),
            Struct(benchmark=1274, date=10),
            Struct(benchmark=1225, date=11),
            Struct(benchmark=1177, date=12),
            Struct(benchmark=1129, date=13),
            Struct(benchmark=1080, date=14),
            Struct(benchmark=1032, date=15),
            Struct(benchmark=983, date=16),
            Struct(benchmark=935, date=17),
            Struct(benchmark=887, date=18),
            Struct(benchmark=838, date=19),
            Struct(benchmark=790, date=20),
            Struct(benchmark=741, date=21),
            Struct(benchmark=693, date=22),
            Struct(benchmark=645, date=23),
            Struct(benchmark=596, date=24),
        ]


def test_build_expected_lines_25th_is_on_weekend():
    # TODO: how do we handle this properly?
    pass
