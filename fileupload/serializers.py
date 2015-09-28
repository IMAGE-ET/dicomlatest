'''
Created on Sep 24, 2015

@author: anilkatta
'''

from rest_framework import serializers
from models import Document
from models import DICOMProperty

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DICOMProperty
        fields = ('prop_key', )

class DICOMPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = DICOMProperty
        fields = ('prop_id', 'prop_key', 'prop_value', 'doc_id')

class DocumentSerializer(serializers.ModelSerializer):
    properties = DICOMPropertySerializer(many=True)
    
    class Meta:
        model = Document
        fields = ('doc_id', 'doc_file', 'date_time', 'properties')
        
    def create(self, validated_data):
        properties = validated_data.pop('properties')
        document = Document.objects.create(**validated_data)
        for prop_data in properties:
            DICOMProperty.objects.create(doc_id=document, **prop_data)
        return document
    
class DocumentListSerializer(serializers.ListSerializer):
    child = DocumentSerializer()
    allow_null = True
    many = True
    
class PropertyListSerializer(serializers.ListSerializer):
    child = PropertySerializer()
    allow_null = True
    many = True