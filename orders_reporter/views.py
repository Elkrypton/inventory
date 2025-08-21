from .modules import *
from .models import Manufacturer
from rest_framework import generics, viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from chatbot.agent import ask_question
import csv
from django.views.decorators.csrf import csrf_exempt
import json
import barcode
import traceback
import io
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
import qrcode
from .forms import SearchForm
from io import BytesIO
import base64
from django.db.models import F
from django.template.loader import get_template
from django.views import View
import xhtml2pdf.pisa as pisa
from .forms import ManufacturerForm
from .models import Manufacturer
from .forms import NoteForm
from django.shortcuts import render, get_object_or_404
from .models import Manufacturer
import matplotlib.pyplot as plt
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from barcode.writer import ImageWriter
from barcode import Code39
from django.db.models import Sum

# def generate_qr_code(sku):
#     code_obj = Code39(sku, writer=ImageWriter())
#     buffer = io.BytesIO()
#     code_obj.write(buffer)
#     buffer.seek(0)
#     barcode_obj, created = GeneratedBarcode.objects.get_or_create(code=sku)
    
#     if created:
#         barcode_obj.image.save(f'{code}.png', buffer, save=True)
#         action_performed = "created"
#     else:
#         action_performed = "fetched"

#     myResponse = f'Barcode "{code}" {action_performed} successfully! <a href="{barcode_obj.image.url}">IMAGE LINK</a>'
    
#     return HttpResponse(myResponse)

@login_required
class TotalNumoProducts():
    """Total number of products"""

    def __init__(self, request):
        """Initialize the class."""
        self.manufacturer = Manufacturer.objects.filter(owner=request.user).values()

    def total_number_of_products(self):
        """Calculate the total number of each product."""
        items_list = [value['item'] for value in self.manufacturer]
        return dict(Counter(items_list))

    def __str__(self):
        """Return a string representation of the class."""
        return "Class includes all products counts and quantity for each"

@method_decorator(login_required, name='dispatch')
class GeneratePDF(View):
    """Class to generate PDF from web page"""

    def get(self, request, *args, **kwargs):
        """Handle GET request for PDF generation."""
        template = get_template('manufacturer_detail.html')
        manufacturer = get_object_or_404(Manufacturer, pk=kwargs['pk'])
        context = {'manufacturer': manufacturer}
        pdf = render_to_pdf('manufacturer_detail.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Manufacturer_{}.pdf".format(manufacturer.id)
            content = "inline; filename={}".format(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename={}".format(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not Found")

@login_required
def qrcode_scanner(request):
    """Handle requests for QR code scanning."""
    return render(request, 'qrcode.html')

@login_required
def product_search(request):
    """Handle product search."""
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            results = Manufacturer.objects.filter(item=query, owner=request.user) | Manufacturer.objects.filter(sku=query, owner=request.user)
        else:
            results = []
    else:
        form = SearchForm()
        results = []
    return render(request, 'search.html', {'form': form, 'results': results})


@login_required
def GraphView(request):
    """Handle rendering of a graph view."""
    total_products = TotalNumoProducts(request)
    item_counts = total_products.total_number_of_products()
    manufacturer = total_products.manufacturer
    products = [values['item'] for values in manufacturer]
    quantities = [values['quantity'] for values in manufacturer]
    items = list(item_counts.keys())
    counts = list(item_counts.values())
    context = {'items': items, 'counts': counts,
               'products': products,
               'quantities': quantities}
    return render(request, 'graph.html', context)

@login_required
def feedback(request):
    """Handle feedback submission."""
    if request.method == 'POST':
        feedback = NoteForm(request.POST)
        if feedback.is_valid():
            print(">> THE FORM IS VALID")
            new_feedback = feedback.save(commit=True)
            # add some extra fields or do some operations
            new_feedback.save()
            return HttpResponseRedirect(reverse('success_page'))
        else:
            print("!!!! THE FORM ISN'T VALID!")
    else:
        feedback = NoteForm()
    return render(request, 'note.html', {'feedback': feedback})


def generate_qr_code(request, pk):
    """Generate a QR code from input data."""
    product = Manufacturer.objects.get(pk=pk)
    url = request.build_absolute_uri(f'/manufacturer/{pk}/')
    qr = qrcode.make(url)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")




@login_required
def manufacturer_edit(request, pk):
    """Handle editing a manufacturer."""

    manufacturer = Manufacturer.objects.get(owner=request.user, pk=pk)
    if request.method != 'POST':
        form = ManufacturerForm(instance=manufacturer)
    else:
        form = ManufacturerForm(instance=manufacturer, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('manufacturer_list'))
    context = {'manufacturer': manufacturer, 'form': form}
    return render(request, 'manufacturer_edit.html', context)


@login_required
def index(request):
    inventory = Manufacturer.objects.filter(owner=request.user)
    low_stock = inventory.filter(quantity__lt=F('low_stock_threshold'))
    total_items = inventory.count()
    total_quantity = inventory.aggregate(Sum('quantity'))['quantity__sum'] or 0
    recent_items = inventory.order_by('-date_of_production')[:5]

    return render(request, 'home.html', {
        'low_stock': low_stock,
        'total_items': total_items,
        'total_quantity': total_quantity,
        'recent_items': recent_items,
    })
@login_required
def render_to_pdf(template_src, context_dict={}):
    """Render a template to a PDF."""
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

@login_required
def my_form_view(request):
    """Handle the form view."""
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            print(">> THE FORM IS VALID")
            item = form.save(commit=False)
            # add some extra fields or do some operations
            item.owner = request.user
            item.save()
            return HttpResponseRedirect(reverse('manufacturer_list'))
        
        else:
            print("!!!! THE FORM ISN'T VALID!")
    else:
        form = ManufacturerForm()
    return render(request, 'forms.html', {'form': form})


def success_page(request):
    """Handle the success page."""
    return render(request, 'submitted.html')


@login_required
def manufacturer_list(request):
    """Handle listing manufacturers."""
    manufacturers = Manufacturer.objects.filter(owner=request.user)
    return render(request, 'manufacturer_list.html',
                  {'manufacturers': manufacturers})

@login_required
def delete_manufacturer(request, pk):
    """Handle deleting a manufacturer."""
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if manufacturer.owner != request.user:
        return HttpResponse("You don't have permission to delete this")
    manufacturer.delete()
    return redirect(reverse('manufacturer_list'))

@login_required
def PurchaseInterface(request):
    return render(request,  'PurchaseInterface.html')

@login_required
def Purchase(request, product, quantity):
    selected_product = Manufacturer.objects.get(item=product)
    selected_product.quantity -= quantity
    selected_product.save()

@login_required
def manufacturer_detail(request, pk):
    """Handle displaying manufacturer details."""
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    if manufacturer.owner != request.user:
        return HttpResponse("You don't have the permission to view this")

 #   file_path = manufacturer.product_img
    #qr_codes = generate_qr_code(manufacturer.sku)
    return render(request, "manufacturer_detail.html",
                  {"manufacturer": manufacturer,
                   })


@api_view(['GET'])
def get_all_products(request):
    products = Manufacturer.objects.all()
    serializer = ManufacturerSerializer(products, many=True)
    return Response(serializer.data)


@login_required
def export_inventory(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'
    writer = csv.writer(response)
    writer.writerow(['Item', 'SKU', 'Quantity'])
    for item in Manufacturer.objects.filter(owner=request.user):
        writer.writerow([item.item, item.sku, item.quantity])
    return response

# ####API SECTION
# class ManufacturerViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing manufacturers."""
#     queryset = Manufacturer.objects.all().order_by('item')
#     serializer_class = ManufacturerSerializer


# class NoteViewSet(viewsets.ModelViewSet):
#     """API endpoint for managing notes."""
#     queryset = Note.objects.all().order_by('name')
#     serializer_class = FeedbackSerializer

# class SearchViewSet(viewsets.ModelViewSet):
#     """API endpoint for searching manufacturers."""
#     queryset = SearchProduct.objects.all()
#     serializer_class = SearchSerializer


