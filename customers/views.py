from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer,PaymentHistory
from .forms import CustomerForm
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
@login_required
def customer_list(request):

    search = request.GET.get('search')

    if search:
        customers = Customer.objects.filter(
            name__icontains=search
        )
    else:
        customers = Customer.objects.all()

    return render(
        request,
        'customer_list.html',
        {'customers': customers}
    )

@login_required
def add_customer(request):

    form = CustomerForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('customer_list')

    return render(
        request,
        'customer_form.html',
        {'form': form}
    )

@login_required
def update_payment(request, pk):

    customer = get_object_or_404(Customer, id=pk)

    if request.method == 'POST':

        amount = Decimal(request.POST['amount'])
        customer.received_payment += amount
        customer.save()
        PaymentHistory.objects.create(
            customer=customer,
            amount=amount
        )
        return redirect('customer_list')

    return render(
        request,
        'update_payment.html',
        {'customer': customer}
    )

@login_required
def delete_customer(request, pk):

    customer = get_object_or_404(Customer, id=pk)

    if customer.remaining_payment <= 0:
        customer.delete()

    return redirect('customer_list')
@login_required
def customer_detail(request, pk):

    customer = Customer.objects.get(id=pk)

    history = PaymentHistory.objects.filter(
        customer=customer
    ).order_by('-payment_date')

    return render(
        request,
        'customer_detail.html',
        {
            'customer': customer,
            'history': history
        }
    )

def register_user(request):

    form = RegisterForm()

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data['password']
            )

            user.save()

            return redirect('login')

    return render(
        request,
        'register.html',
        {'form': form}
    )
def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('customer_list')

    return render(
        request,
        'login.html'
    )
def logout_user(request):

    logout(request)

    return redirect('login')