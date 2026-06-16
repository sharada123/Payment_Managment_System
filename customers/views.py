from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer,PaymentHistory
from .forms import CustomerForm,AddServiceForm,RegisterForm
from decimal import Decimal
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
@login_required
def customer_list(request):

    search = request.GET.get('search')

    customers = Customer.objects.all()

    if search:
        customers = customers.filter(
            name__icontains=search
        )

    print("Search:", search)
    print("Count:", customers.count())

    return render(
        request,
        'customer_list.html',
        {'customers': customers}
    )

@login_required
def dashboard(request):

    customers = Customer.objects.all()

    total_customers = customers.count()

    pending_customers = customers.filter(
        total_fees__gt=F('received_payment')
    ).count()

    total_received = customers.aggregate(
        Sum('received_payment')
    )['received_payment__sum'] or 0

    total_fees = customers.aggregate(
        Sum('total_fees')
    )['total_fees__sum'] or 0

    total_pending_amount = total_fees - total_received

    context = {
        'total_customers': total_customers,
        'pending_customers': pending_customers,
        'total_received': total_received,
        'total_pending_amount': total_pending_amount,
    }

    return render(
        request,
        'dashboard.html',
        context
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

            return redirect('dashboard')

    return render(
        request,
        'login.html'
    )
def logout_user(request):

    logout(request)

    return redirect('login')

@login_required
def add_service(request, pk):

    customer = get_object_or_404(
        Customer,
        id=pk
    )

    form = AddServiceForm()

    if request.method == 'POST':

        form = AddServiceForm(request.POST)

        if form.is_valid():

            service_name = form.cleaned_data['service_name']
            service_fee = form.cleaned_data['service_fee']

            if customer.tasks:

                customer.tasks += f"\n{service_name}"

            else:

                customer.tasks = service_name

            customer.total_fees += service_fee

            customer.save()

            return redirect(
                'customer_list',
            
            )

    return render(
        request,
        'add_service.html',
        {
            'customer': customer,
            'form': form
        }
    )
@login_required
def download_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customers.pdf"'

    pdf = SimpleDocTemplate(
    response,
    pagesize=landscape(letter)
)
    customers = Customer.objects.all()

    data = [
        [
            'Name',
            'Mobile No',
            'Services',
            'Total Fees',
            'Received ',
            'Pending '
        ]
    ]

    for c in customers:

        data.append([
            c.name.upper(),
            c.mobile,
            c.tasks.upper(),
            str(c.total_fees),
            str(c.received_payment),
            str(c.remaining_payment)
        ])

    table = Table(data,colWidths=[120,70,180,70,70,70])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
    ]))

    pdf.build([table])

    return response