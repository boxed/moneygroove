from django.contrib.auth import authenticate
from django.db.models import Sum
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.utils.formats import localize
from django.utils.timezone import now
from django.views.decorators.http import require_POST
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


def build_expected_lines(*, sum_income, sum_expenses, expenses, target_savings):
    after_expected_expenses = sum_income - sum_expenses - target_savings
    per_day = after_expected_expenses / 30
    dates = [
        30 + x if x <= 0 else x
        for x in range(-5, 25)
    ]

    def passed_date(x, i):
        if x > 30:
            x = 30
        return dates.index(x) <= i

    return [
        Struct(
            date=date,
            benchmark=localize(int(
                sum_income
                - (per_day * i)  # per day to reach end
                - sum([x.amount for x in expenses if passed_date(x.expected_date, i)])  # expenses predicted to have been hit
            )),
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
    )


class IndexPage(Page):
    class Meta:
        title = 'Money groove'

        @staticmethod
        def extra_params(request):
            return groove(request.user)

    today = html.h2(lambda params, **_: params.today)

    sum_income = html.div(lambda params, **_: f'Sum income: {params.sum_income}')
    sum_expenses = html.div(lambda params, **_: f'Sum initial expenses: {params.sum_expenses}')

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


def api__groove(request):
    username = request.headers.get('x-username')
    password = request.headers.get('x-password')
    if username is None or password is None:
        return HttpResponseBadRequest()

    user = authenticate(username=username, password=password)
    return JsonResponse(groove(user))
