import traceback

try:
    
    from django.shortcuts import render
    from django.shortcuts import redirect
    from django.shortcuts import HttpResponseRedirect, reverse, HttpResponse
    from django.contrib.auth.decorators import login_required
    import qrcode
    from .forms import SearchForm
    from io import BytesIO
    import base64
    from django.template.loader import get_template
    from django.views import View
    import xhtml2pdf.pisa as pisa
    from .forms import ManufacturerForm, NoteForm
    from .models import Manufacturer
    from django.shortcuts import render, get_object_or_404
    from .models import Manufacturer
    import matplotlib.pyplot as plt
    from collections import Counter
    from django.contrib.auth.decorators import permission_required


except ImportError as err:
    print("----IMPORT ERROR --->\n---> {}".format(err))
    traceback.print_exc()