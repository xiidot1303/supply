from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.models import *
from app.services import statementservice, supplyservice, supplierservice

@login_required
def statement_list_all(request):
    sts = Statement.objects.filter().exclude(status=None).order_by('-date')
    context = {'list': sts}
    return render(request, 'statement/statement_list.html', context)

@login_required
def statement_supplies(request, pk):
    statement = statementservice.get_object_by_id(pk)
    supplies = supplyservice.filter_supplies_by_statement(statement)
    context = {'list': supplies, 'statement_id': pk}
    return render(request, 'statement/statement_supplies.html', context)

@login_required
def statement_accept_supply(request, pk):
    obj = supplyservice.get_object_by_id(pk)
    if obj.statement.status != 'end':
        supplyservice.confirm_supply(obj)
    return redirect(statement_supplies, pk=obj.statement.pk)

@login_required
def statement_cancel(request, pk):
    statementservice.cancel_statement_by_id(pk)
    return redirect(statement_list_all)
