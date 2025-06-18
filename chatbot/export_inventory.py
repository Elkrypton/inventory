# chatbot/export_inventory.py

import os
import sys
import django

# 👇 Ensure Python can find your project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 👇 Match this to the folder where your `settings.py` lives
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orders_report.settings")
django.setup()

from orders_reporter.models import Manufacturer

def export_inventory_data():
    products = Manufacturer.objects.all()
    documents = []

    for p in products:
# export_inventory.py
        content = (
            f"Item: {p.item}\n"
            f"SKU: {p.sku}\n"
            f"Date of Production: {p.date_of_production}\n"
            f"Location: {p.location}\n"
            f"Quantity: {p.quantity}\n"
            "------"
        )

        documents.append(content)

    return documents
