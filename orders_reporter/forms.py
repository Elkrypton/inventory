import random
from django import forms
from .models import Manufacturer, Note, SearchProduct

CHOICES = (('GenerateSku', 'generate_sku'), ('Add Manually', 'add_manually'))


class ManufacturerForm(forms.ModelForm):
    sku_gen = forms.ChoiceField(choices=[('auto', 'Generate Automatically'), ('manual', 'Enter Manually')],
    widget=forms.RadioSelect()
    )


    class Meta:

        """meta class to customize model forms for the manufacturer model"""
        model = Manufacturer
        sku_gen = forms.ChoiceField(choices = CHOICES, widget=forms.RadioSelect())
        fields = ['item', 'quantity', 'date_of_production', 'sku', 'location']
        widgets = {

            'item': forms.TextInput(attrs={'size': '40', 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'sixze': '40', 'class': 'form-control'}),
            'date_of_production': forms.widgets.DateInput(attrs={'type': 'date'}),

            'sku': forms.TextInput(attrs={'size': '40', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'size': '40', 'class': 'form-control'})}
        


    def clean_sku(self):
        """Returns random generated sku"""
        sku_type = self.cleaned_data.get('sku_gen')
        if sku_type == 'auto':
            while True:
                sku = f"{random.randint(1000, 9999)}-{random.randint(0, 999):03d}-\
                        {random.randint(0, 9999):04d}"
                if not Manufacturer.objects.filter(sku=sku).exists():
                    return sku
        else:
            sku = self.cleaned_data.get('sku')
            return sku


class NoteForm(forms.ModelForm):

    class Meta:
        """Meta class to cutomize note model."""

        model = Note
        fields = ['name', 'feedback']
        widgets = {
                        'name':forms.TextInput(attrs={'size': '40', 'class': 'form-control'}),
                        'feedback': forms.Textarea()
                }


class SearchForm(forms.ModelForm):

    class Meta:
        """Meta class to cutomize search model"""

        model = SearchProduct
        fields = ['query']
        widgets = {
        'query':forms.TextInput(attrs={'size':'40', 'class': 'form-control'})}

