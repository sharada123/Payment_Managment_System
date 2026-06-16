from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    tasks = models.TextField(blank=True)
    mobile = models.CharField(max_length=10,blank=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2)
    received_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def remaining_payment(self):
        return self.total_fees - self.received_payment

    def __str__(self):
        return self.name

class PaymentHistory(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer.name} - ₹{self.amount}"