# invoice/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Invoice
from transactions.models import Sale, SalesOrderDetail
from django.core.paginator import Paginator

def generate_invoice_view(request):
    generated_invoice = None
    error_message = None

    if request.method == "POST":
        sale_id = request.POST.get('sale_id')
        sale = get_object_or_404(Sale, pk=sale_id)

        if Invoice.objects.filter(sale=sale).exists():
            error_message = f"An invoice for Sale Order {sale_id} - {sale.customer_id.first_name} {sale.customer_id.last_name} already exists."
        else:
            invoice = Invoice.objects.create(sale=sale)
            sale.payment_status = 'Paid'  # Update payment status to Paid
            sale.save()
            generated_invoice = {
                'sale_id': sale.id,
                'customer_name': f"{sale.customer_id.first_name} {sale.customer_id.last_name}"
            }
            return redirect(f"{request.path}?generated={generated_invoice['sale_id']}&customer={generated_invoice['customer_name']}")

    sales = Sale.objects.all()  # Fetch all sales orders
    invoices = Invoice.objects.all()

    # Pagination logic
    paginator = Paginator(invoices, 10)  # Show 10 invoices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'invoice/generate_invoice.html', {
        'sales': sales,
        'page_obj': page_obj,
        'generated_invoice': generated_invoice,
        'error_message': error_message
    })

def invoice_list_view(request):
    invoices = Invoice.objects.all()
    paginator = Paginator(invoices, 10)  # Show 10 invoices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'invoice/invoicelist.html', {'page_obj': page_obj})

def invoice_detail_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = SalesOrderDetail.objects.filter(sale=invoice.sale)
    subtotal = items.aggregate(total=models.Sum('subtotal'))['total'] or 0
    context = {
        'invoice': invoice,
        'items': items,
        'subtotal': subtotal,
    }
    return render(request, 'invoice/invoice_detail.html', context)

def delete_invoice_view(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('generate-invoice')
    return render(request, 'invoice/invoice_confirm_delete.html', {'invoice': invoice})
