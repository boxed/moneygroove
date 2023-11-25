import calendar
from datetime import (
    datetime,
    timedelta,
)

from django.contrib.auth import authenticate
from django.db.models import Sum
from django.http import (
    HttpResponseBadRequest,
    JsonResponse,
)
from django.utils.formats import localize
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from iommi import (
    Column,
    EditColumn,
    EditTable,
    Form,
    html,
    Page,
    Table,
)
from iommi.struct import Struct

from moneygroove.models import (
    ExpectedExpense,
    ExpectedIncome,
    User,
)


def previous_month_length():
    return (datetime.now().replace(day=1) - timedelta(days=1)).day


def current_month_length():
    now = datetime.now()
    return calendar.monthrange(now.year, now.month)[1]


def build_expected_lines(*, sum_income, sum_expenses, expenses, target_savings):
    end_of_month = previous_month_length() if datetime.now().day < 25 else current_month_length()

    after_expected_expenses = sum_income - sum_expenses - target_savings
    per_day = after_expected_expenses / end_of_month

    dates = [
        end_of_month + x if x <= 0 else x
        for x in range(-5, 25)
    ]

    def passed_date(x, i):
        if x > end_of_month:
            x = end_of_month
        return dates.index(x) <= i

    return [
        Struct(
            date=date,
            benchmark=int(
                sum_income
                - (per_day * i)  # per day to reach end
                - sum([x.amount for x in expenses if passed_date(x.expected_date, i)])  # expenses predicted to have been hit
            ),
        )
        for i, date in enumerate(dates)
    ]


def groove(user):
    sum_income = ExpectedIncome.objects.filter(user=user).aggregate(sum=Sum('amount'))['sum'] or 0
    sum_expenses = ExpectedExpense.objects.filter(user=user).aggregate(sum=Sum('amount'))['sum'] or 0
    expected_lines = build_expected_lines(sum_income=sum_income, sum_expenses=sum_expenses, expenses=ExpectedExpense.objects.filter(user=user), target_savings=user.target_savings)
    benchmark_by_date = {
        x.date: x.benchmark
        for x in expected_lines
    }

    return dict(
        sum_income=sum_income,
        sum_expenses=sum_expenses,
        expected_lines=expected_lines,
        today=benchmark_by_date[now().day],
        benchmark_by_date=benchmark_by_date,
    )


class IndexPage(Page):
    class Meta:
        title = 'Money groove'

        @staticmethod
        def extra_params(request):
            return groove(request.user)

    today = html.h2(lambda params, **_: localize(params.today))

    sum_income = html.div(lambda params, **_: f'Sum income: {localize(params.sum_income)}')
    sum_expenses = html.div(lambda params, **_: f'Sum initial expenses: {localize(params.sum_expenses)}')

    expected = Table(
        rows=lambda params, **_: params.expected_lines,
        columns=dict(
            date=Column.integer(),
            benchmark=Column.integer(),
        ),
        page_size=None,
    )

    settings = Form.edit(
        title='Settings',
        auto__model=User,
        auto__include=['target_savings'],
        instance=lambda request, **_: request.user,
    )

    income = EditTable(
        auto__model=ExpectedIncome,
        auto__include=['name', 'amount', 'expected_date', 'user'],
        rows=lambda request, **_: ExpectedIncome.objects.filter(user=request.user),
        columns=dict(
            name__edit__include=True,
            amount__edit__include=True,
            expected_date__edit__include=True,
        ),
        columns__user=EditColumn.hardcoded(
            render_column=False,
            edit__parsed_data=lambda request, **_: request.user,
        ),
    )

    expenses = EditTable(
        auto__model=ExpectedExpense,
        auto__include=['name', 'amount', 'expected_date', 'user'],
        rows=lambda request, **_: ExpectedExpense.objects.filter(user=request.user),
        columns=dict(
            name__edit__include=True,
            amount__edit__include=True,
            expected_date__edit__include=True,
        ),
        columns__user=EditColumn.hardcoded(
            render_column=False,
            edit__parsed_data=lambda request, **_: request.user,
        ),
    )


@csrf_exempt
def api__groove(request):
    username = request.headers.get('x-username')
    password = request.headers.get('x-password')
    if username is None or password is None:
        return HttpResponseBadRequest()

    user = authenticate(username=username, password=password)
    return JsonResponse(groove(user))
