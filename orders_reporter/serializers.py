from rest_framework import serializers 
from .models import Manufacturer, Note, SearchProduct



class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchProduct
        fields = '__all__'
