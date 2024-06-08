from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PurchaseOrder, PurchaseOrderDetail, Sale, Item, SalesOrderDetail
from .forms import PurchaseOrderForm, PurchaseOrderDetailForm, SaleForm, SalesOrderDetailForm
from accounts.models import Profile
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from .tables import PurchaseOrderTable, SaleTable
from django.db.models import Count, Sum
from django.http import HttpResponse
import tablib
from django.db import transaction 
import logging
from django.contrib import messages

from django.http import JsonResponse
from .models import Sale
from django.db.models import Count
from django.utils import timezone
import datetime
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

@login_required
def get_sales_orders_data(request):
    today = timezone.now()
    one_year_ago = today - datetime.timedelta(days=365)
    sales = Sale.objects.filter(order_date__gte=one_year_ago).extra(select={'month': "strftime('%%Y-%%m', order_date)"}).values('month').annotate(total_sales=Count('id')).order_by('month')
    data = {
        "labels": [sale['month'] for sale in sales],
        "values": [sale['total_sales'] for sale in sales]
    }
    return JsonResponse(data)

class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'transactions/purchases_list.html'
    context_object_name = 'purchase_orders'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            item_count=Count('purchaseorderdetail'),
            total_due=Sum('purchaseorderdetail__subtotal')
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for purchase in context['purchase_orders']:
            purchase.item_count = purchase.purchaseorderdetail_set.count()
        return context

    def get(self, request, *args, **kwargs):
        if '_export' in request.GET:
            return self.export_purchases()
        return super().get(request, *args, **kwargs)

    def export_purchases(self):
        purchases = self.get_queryset()
        dataset = tablib.Dataset()
        dataset.headers = ['ID', 'Supplier', 'Order Date', 'Delivery Date', 'Delivery Status', 'Total Amount Due', 'Payment Method', 'Payment Status', 'Items']
        
        for purchase in purchases:
            dataset.append([
                purchase.purchase_order_id, 
                purchase.supplier_id.name,
                purchase.order_date, 
                purchase.delivery_date, 
                purchase.delivery_status, 
                purchase.total_due, 
                purchase.payment_method, 
                purchase.payment_status, 
                purchase.purchaseorderdetail_set.count()
            ])
        
        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="purchase_orders.xlsx"'
        return response

class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'transactions/purchasescreate.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.items = PurchaseOrderDetail.objects.filter(purchase_order_id=self.object).count()
        total_due = PurchaseOrderDetail.objects.filter(purchase_order_id=self.object).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        self.object.total_amount_due = total_due
        self.object.save()
        return response

    def get_success_url(self):
        return reverse('purchases_detail_create', kwargs={'pk': self.object.pk})

class PurchaseOrderDetailView(DetailView):
    model = PurchaseOrder
    template_name = 'transactions/purchasedetail.html'
    context_object_name = 'purchase_order'

class PurchaseOrderUpdateView(UpdateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'transactions/purchaseupdate.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.items = PurchaseOrderDetail.objects.filter(purchase_order_id=self.object).count()
        total_due = PurchaseOrderDetail.objects.filter(purchase_order_id=self.object).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        self.object.total_amount_due = total_due
        self.object.save()
        return response

    def get_success_url(self):
        return reverse('purchases_detail', kwargs={'pk': self.object.pk})

class PurchaseOrderDeleteView(DeleteView):
    model = PurchaseOrder
    template_name = 'transactions/purchasedelete.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        PurchaseOrderDetail.objects.filter(purchase_order_id=self.object).delete()
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('purchases_list')

class PurchaseOrderDetailViewList(ListView):
    model = PurchaseOrderDetail
    template_name = 'transactions/purchase_detail_view.html'
    context_object_name = 'purchase_order_details'

    def get_queryset(self):
        purchase_order_id = self.kwargs['pk']
        return PurchaseOrderDetail.objects.filter(purchase_order_id=purchase_order_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        total_due = self.get_queryset().aggregate(Sum('subtotal'))['subtotal__sum'] or 0
        purchase_order = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
        purchase_order.total_amount_due = total_due
        purchase_order.save()
        return context

class PurchaseOrderDetailCreateView(CreateView):
    model = PurchaseOrderDetail
    form_class = PurchaseOrderDetailForm
    template_name = 'transactions/add_purchase_item.html'

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.purchase_order_id_id = self.kwargs['pk']
            item = form.instance.item
            new_quantity = item.quantity + form.instance.quantity

            if new_quantity < 0:
                messages.error(self.request, "Invalid Input: Quantity cannot be less than zero.")
                return self.form_invalid(form)

            response = super().form_valid(form)
            item.quantity = new_quantity
            item.save()
            purchase_order = PurchaseOrder.objects.get(pk=self.kwargs['pk'])
            purchase_order.items = PurchaseOrderDetail.objects.filter(purchase_order_id=purchase_order).count()
            total_due = PurchaseOrderDetail.objects.filter(purchase_order_id=purchase_order).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            purchase_order.total_amount_due = total_due
            purchase_order.save()
        return response

    def get_success_url(self):
        return reverse('purchases_detail_view', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.all()
        context['purchase_order'] = get_object_or_404(PurchaseOrder, pk=self.kwargs['pk'])
        context['pk'] = self.kwargs['pk']
        return context

class PurchaseOrderDetailUpdateView(UpdateView):
    model = PurchaseOrderDetail
    form_class = PurchaseOrderDetailForm
    template_name = 'transactions/edit_purchase_item.html'

    def form_valid(self, form):
        with transaction.atomic():
            old_detail = PurchaseOrderDetail.objects.get(pk=self.object.pk)
            item = form.instance.item
            new_quantity = item.quantity - old_detail.quantity + form.instance.quantity

            if new_quantity < 0:
                messages.error(self.request, "Invalid Input: Quantity cannot be less than zero.")
                return self.form_invalid(form)

            item.quantity = new_quantity
            response = super().form_valid(form)
            item.save()
            purchase_order = PurchaseOrder.objects.get(pk=self.object.purchase_order_id.pk)
            purchase_order.items = PurchaseOrderDetail.objects.filter(purchase_order_id=purchase_order).count()
            total_due = PurchaseOrderDetail.objects.filter(purchase_order_id=purchase_order).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            purchase_order.total_amount_due = total_due
            purchase_order.save()
        return response

    def get_success_url(self):
        return reverse('purchases_detail_view', kwargs={'pk': self.kwargs['pk']})

class PurchaseOrderDetailDeleteView(DeleteView):
    model = PurchaseOrderDetail
    template_name = 'transactions/delete_purchase_item.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        item = self.object.item
        logger.debug(f"Item quantity before deletion: {item.quantity}")
        item.quantity -= self.object.quantity
        item.save()
        logger.debug(f"Item quantity after deletion: {item.quantity}")
        self.object.delete()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('purchases_detail_view', kwargs={'pk': self.object.purchase_order_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail'] = self.object  
        return context

class SaleListView(ListView):
    model = Sale
    template_name = 'transactions/sales_list.html'
    context_object_name = 'sales'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        queryset = queryset.annotate(
            items_count=Sum('order_details__quantity'),
            calculated_total_due=Sum('order_details__subtotal') + Sum('shipping_fee')  # Ensure shipping fee is included
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for sale in context['sales']:
            sale.items_count = sale.order_details.count()
        return context

    def get(self, request, *args, **kwargs):
        if '_export' in request.GET:
            return self.export_sales()
        return super().get(request, *args, **kwargs)

    def export_sales(self):
        sales = self.get_queryset()
        dataset = tablib.Dataset()
        dataset.headers = ['ID', 'Customer', 'Logistics', 'Order Type', 'Order Date', 'Delivery Date', 'Sales Order Status', 'Shipping Fee', 'Total Amount Due', 'Payment Type', 'Payment Status', 'Items']

        for sale in sales:
            dataset.append([
                sale.id,
                f"{sale.customer_id.first_name} {sale.customer_id.last_name}",
                sale.logistics_id.company,
                sale.order_type,
                sale.order_date,
                sale.delivery_date,
                sale.sales_order_status,
                sale.shipping_fee,
                sale.calculated_total_due,
                sale.payment_type,
                sale.payment_status,
                sale.items_count
            ])

        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="sales_orders.xlsx"'
        return response

class SaleDetailView(DetailView):
    model = Sale
    template_name = 'transactions/saledetail.html'
    context_object_name = 'sale'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = self.get_object()
        sale_details = SalesOrderDetail.objects.filter(sale=sale)
        total_due = sale_details.aggregate(total=Sum('subtotal'))['total'] or 0
        context['sale_details'] = sale_details
        context['calculated_total_due'] = total_due
        return context
        
class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'transactions/salescreate.html'

    def form_valid(self, form):
        form.instance.payment_status = 'Unpaid'
        response = super().form_valid(form)
        self.object.update_total_amount_due()
        return response

    def get_success_url(self):
        return reverse('salesitems-list', kwargs={'sale_id': self.object.id})

class SaleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sale
    template_name = 'transactions/sale_update.html'
    form_class = SaleForm

    def test_func(self):
        profiles = Profile.objects.all()
        if self.request.user.profile in profiles:
            return True
        else:
            return False

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.update_total_amount_due()
        return response

    def get_success_url(self):
        return reverse('saleslist')
    
class SaleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sale
    template_name = 'transactions/saledelete.html'

    def get_success_url(self):
        return reverse('saleslist')

    def test_func(self):
        return self.request.user.is_superuser

class SalesOrderDetailViewList(ListView):
    model = SalesOrderDetail
    template_name = 'transactions/salesitems_list.html'
    context_object_name = 'order_details'

    def get_queryset(self):
        sale_id = self.kwargs['sale_id']
        return SalesOrderDetail.objects.filter(sale_id=sale_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = get_object_or_404(Sale, id=self.kwargs['sale_id'])
        return context

class SalesOrderDetailCreateView(CreateView):
    model = SalesOrderDetail
    form_class = SalesOrderDetailForm
    template_name = 'transactions/create_salesorder_item.html'

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.sale_id = self.kwargs['sale_id']
            item = form.instance.item
            new_quantity = item.quantity - form.instance.quantity

            if new_quantity < 0:
                messages.error(self.request, "Invalid Input: Quantity cannot be less than zero.")
                return self.form_invalid(form)

            response = super().form_valid(form)
            item.quantity = new_quantity
            item.save()
            sale = Sale.objects.get(pk=self.kwargs['sale_id'])
            sale.items = SalesOrderDetail.objects.filter(sale_id=sale).count()
            total_due = SalesOrderDetail.objects.filter(sale_id=sale).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            sale.total_amount_due = total_due
            sale.save()
        return response

    def get_success_url(self):
        return reverse('salesitems-list', kwargs={'sale_id': self.kwargs['sale_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = get_object_or_404(Sale, id=self.kwargs['sale_id'])
        return context

class SalesOrderDetailUpdateView(UpdateView):
    model = SalesOrderDetail
    form_class = SalesOrderDetailForm
    template_name = 'transactions/update_salesorder_item.html'

    def form_valid(self, form):
        with transaction.atomic():
            old_detail = SalesOrderDetail.objects.get(pk=self.object.pk)
            item = form.instance.item
            new_quantity = item.quantity + old_detail.quantity - form.instance.quantity

            if new_quantity < 0:
                messages.error(self.request, "Invalid Input: Quantity cannot be less than zero.")
                return self.form_invalid(form)

            item.quantity = new_quantity
            response = super().form_valid(form)
            item.save()
            sale = Sale.objects.get(pk=self.object.sale_id)
            sale.items = SalesOrderDetail.objects.filter(sale_id=sale).count()
            total_due = SalesOrderDetail.objects.filter(sale_id=sale).aggregate(Sum('subtotal'))['subtotal__sum'] or 0
            sale.total_amount_due = total_due
            sale.save()
        return response

    def get_success_url(self):
        return reverse('salesitems-list', kwargs={'sale_id': self.object.sale.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sale'] = self.object.sale
        context['sale_id'] = self.object.sale.id
        return context

class SalesOrderDetailDeleteView(DeleteView):
    model = SalesOrderDetail
    template_name = 'transactions/delete_salesorder_item.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        sale_id = self.object.sale.id
        item = self.object.item
        item.quantity += self.object.quantity
        item.save()
        self.object.delete()
        return redirect(self.get_success_url(sale_id))

    def get_success_url(self, sale_id):
        return reverse('salesitems-list', kwargs={'sale_id': sale_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detail'] = self.object
        context['sale_id'] = self.object.sale.id
        return context

def generate_invoice_view(request):
    if request.method == "POST":
        sale_id = request.POST.get('sale_id')
        sale = get_object_or_404(Sale, pk=sale_id)
        return redirect('generate-invoice')

    sales = Sale.objects.filter(sales_order_status='Finished')
    return render(request, 'transactions/generate_invoice.html', {
        'sales': sales,
    })