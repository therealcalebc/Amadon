from django.shortcuts import render, redirect
from decimal import Decimal
from .models import Order, Product

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    item_from_form = Product.objects.get(id=int(request.POST['product_id']))
    quantity_from_form = int(request.POST["quantity"])
    # price_from_form = float(request.POST["price"])
    total_charge = item_from_form.price * quantity_from_form
    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
    request.session['last_charged_amount'] = str(total_charge)
    if 'total_items_ordered' in request.session:
        request.session['total_items_ordered'] = str(int(request.session['total_items_ordered']) + quantity_from_form)
    else:
        request.session['total_items_ordered'] = str(quantity_from_form)
    if 'total_money_spent' in request.session:
        request.session['total_money_spent'] = str(Decimal(request.session['total_money_spent']) + total_charge)
    else:
        request.session['total_money_spent'] = str(total_charge)
    return redirect('/confirmed')

def confirmed(request):
    context = {}
    if 'last_charged_amount' in request.session:
        context['amount_charged'] = request.session['last_charged_amount']
    if 'total_items_ordered' in request.session:
        context['total_items'] = request.session['total_items_ordered']
    if 'total_money_spent' in request.session:
        context['total_spent'] = request.session['total_money_spent']
    return render(request, "store/success.html", context)
