"""
Module: store.views

Contains Django views for managing items, profiles, deliveries, and customers in the store application.

Classes handle product listing, creation, updating, deletion, and delivery management.
The module integrates with Django's authentication and querying functionalities.
"""
import operator
from functools import reduce
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from django.db.models import Q, Count, Sum
from django.views.generic.edit import FormMixin

from accounts.models import Profile
from transactions.models import Sale
from .models import Category, Item, Delivery, Customer
from .forms import ProductForm, CustomerForm, DeliveryForm
from .tables import ItemTable, CustomerTable
from .models import Supplier, Customer

from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from .models import Delivery
from .tables import DeliveryTable
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import ListView
from django_tables2.export.export import TableExport

from django.http import JsonResponse
from django.db.models import Sum
from .models import Item

@login_required
def get_product_stock_data(request):
    items = Item.objects.values('category__name').annotate(total_quantity=Sum('quantity'))
    data = {
        "labels": [item['category__name'] for item in items],
        "values": [item['total_quantity'] for item in items]
    }
    return JsonResponse(data)

@login_required
def dashboard(request):
    """
    View function to render the dashboard with item and profile data.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template with dashboard data.
    """
    profiles =  Profile.objects.all()
    Category.objects.annotate(nitem=Count('item'))
    items = Item.objects.all()
    total_items = Item.objects.all().aggregate(Sum('quantity')).get('quantity__sum', 0.00)
    items_count = items.count()
    profiles_count = profiles.count()

    #profile pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(profiles, 3)
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    #items pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(items, 4)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {
        'items': items,
        'profiles' : profiles,
        'profiles_count': profiles_count,
        'items_count': items_count,
        'total_items': total_items,
        'supplier' : Supplier.objects.all(),
        'delivery': Delivery.objects.all(),
        'sales': Sale.objects.all()
    }
    return render(request, 'store/dashboard.html', context)

class ProductListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    """
    View class to display a list of products.

    Attributes:
    - model: The model associated with the view.
    - table_class: The table class used for rendering.
    - template_name: The HTML template used for rendering the view.
    - context_object_name: The variable name for the context object.
    - paginate_by: Number of items per page for pagination.
    """
    model = Item
    table_class = ItemTable
    template_name = 'store/productslist.html'
    context_object_name = 'items'
    paginate_by = 10
    SingleTableView.table_pagination = False

class ItemSearchListView(ProductListView):
    """
    View class to search and display a filtered list of items.

    Attributes:
    - paginate_by: Number of items per page for pagination.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(ItemSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list))
            )
        return result

class ProductDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """
    View class to display detailed information about a product.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    """
    model = Item
    template_name = 'store/productdetail.html'

    def get_success_url(self):
        return reverse('product-detail', kwargs={'slug': self.object.slug})

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    View class to create a new product.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - form_class: The form class used for data input.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Item
    template_name = 'store/productcreate.html'
    form_class = ProductForm
    success_url = '/products'

    def test_func(self):
        #item = Item.objects.get(id=pk)
        if self.request.POST.get("quantity") < 1:
            return False
        else:
            return True

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View class to update product information.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - fields: The fields to be updated.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Item
    template_name = 'store/productupdate.html'
    fields = ['name','category','quantity','selling_price', 'expiring_date', 'supplier']
    success_url = '/products'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View class to delete a product.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful deletion.
    """
    model = Item
    template_name = 'store/productdelete.html'
    success_url = '/products'


    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

class DeliveryListView(LoginRequiredMixin, SingleTableView):
    """
    View class to display a list of deliveries.

    Attributes:
    - model: The model associated with the view.
    - table_class: The table class for rendering the deliveries.
    - pagination: Number of items per page for pagination.
    - template_name: The HTML template used for rendering the view.
    - context_object_name: The variable name for the context object.
    """
    model = Delivery
    table_class = DeliveryTable
    paginate_by = 10
    template_name = 'store/deliveries.html'
    context_object_name = 'deliveries'

    def get_table_data(self):
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_table()
        export_format = self.request.GET.get('_export', None)
        if 'export' in self.request.GET and export_format:
            exporter = TableExport(export_format, table)
            context['file'] = exporter.export_stream()
            context['file_type'] = export_format
        return context
    
class DeliverySearchListView(DeliveryListView):
    """
    View class to search and display a filtered list of deliveries.

    Attributes:
    - paginate_by: Number of items per page for pagination.
    """
    paginate_by = 10

    def get_queryset(self):
        result = super(DeliverySearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(customer_name__icontains=q) for q in query_list))
            )
        return result

class DeliveryDetailView(LoginRequiredMixin, DetailView):
    """
    View class to display detailed information about a delivery.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    """
    model = Delivery
    template_name = 'store/deliverydetail.html'
    
    def get_object(self, queryset=None):
        return Delivery.objects.get(pk=self.kwargs.get("pk"))
class DeliveryCreateView(LoginRequiredMixin, CreateView):
    """
    View class to create a new delivery.

    Attributes:
    - model: The model associated with the view.
    - form_class: The form class to be used for rendering the view.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Delivery
    form_class = DeliveryForm  # Replace DeliveryForm with the actual form class name
    template_name = 'store/deliveriescreate.html'
    success_url = '/deliveries'

class DeliveryUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update delivery information.

    Attributes:
    - model: The model associated with the view.
    - fields: The fields to be updated.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Delivery
    template_name = 'store/deliveryupdate.html'
    fields = ['company', 'contact_number', 'email_address', 'street', 'barangay', 'city', 'zip_code', 'province', 'country']
    success_url = '/deliveries'

class DeliveryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View class to delete a delivery.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful deletion.
    """
    model = Delivery
    template_name = 'store/productdelete.html'
    success_url = '/deliveries'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        else:
            return False

class SupplierListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    """
    View class to display a list of suppliers.

    Attributes:
    - model: The model associated with the view.
    - pagination: Number of items per page for pagination.
    - template_name: The HTML template used for rendering the view.
    - context_object_name: The variable name for the context object.
    """
    model = Supplier
    pagination = 10
    template_name = 'store/supplierlist.html'  # Assuming the template name is 'suppliers.html'
    context_object_name = 'suppliers'

class SupplierCreateView(LoginRequiredMixin, CreateView):
    """
    View class to create a new supplier.
    """
    model = Supplier
    fields = ['name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country']
    template_name = 'store/suppliercreate.html'
    success_url = '/suppliers'

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update supplier information.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - fields: The fields to be updated.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Supplier
    fields = ['name', 'phone_number', 'email', 'address_line_one', 'city', 'province', 'zip_code', 'country']
    template_name = 'store/supplierupdate.html'
    success_url = '/suppliers'

    def test_func(self):
        """
        Check if the user is a superuser.
        """
        return self.request.user.is_superuser

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    """
    View class to delete a supplier.
    """
    model = Supplier
    template_name = 'store/supplierdelete.html'
    success_url = '/suppliers'
    
class CustomerListView(LoginRequiredMixin, ExportMixin, tables.SingleTableView):
    """
    View class to display a list of customers.

    Attributes:
    - model: The model associated with the view.
    - table_class: The table class used for rendering.
    - template_name: The HTML template used for rendering the view.
    - context_object_name: The variable name for the context object.
    - paginate_by: Number of items per page for pagination.
    """
    model = Customer
    table_class = CustomerTable
    template_name = 'store/customerlist.html'
    context_object_name = 'customers'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('customer_id')
        return queryset

class CustomerCreateView(LoginRequiredMixin, CreateView):
    """
    View class to create a new customer.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - form_class: The form class used for data input.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Customer
    template_name = 'store/customercreate.html'
    form_class = CustomerForm
    success_url = '/customers'

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update customer information.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - fields: The fields to be updated.
    - success_url: The URL to redirect to upon successful form submission.
    """
    model = Customer
    template_name = 'store/customerupdate.html'
    form_class = CustomerForm
    success_url = '/customers'

class CustomerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View class to delete a customer.

    Attributes:
    - model: The model associated with the view.
    - template_name: The HTML template used for rendering the view.
    - success_url: The URL to redirect to upon successful deletion.
    """
    model = Customer
    template_name = 'store/customerdelete.html'
    success_url = '/customers'

    def test_func(self):
        return self.request.user.is_superuser

# Add this function to handle customer details
@login_required
def customer_detail(request, pk):
    """
    View function to display detailed information about a customer.

    Args:
    - request: HttpRequest object.
    - pk: Primary key of the customer to be detailed.

    Returns:
    - Rendered template with customer details.
    """
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'store/customer_detail.html', {'customer': customer})