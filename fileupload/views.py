from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
import datetime

from models import Document, DICOMProperty
from serializers import DocumentListSerializer, DocumentSerializer, PropertyListSerializer
import dicom
import uuid

from rest_framework.parsers import MultiPartParser, FormParser

class DocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser, )
    def post(self, request, format=None):
        my_file = request.FILES['file']
        file_name = str(uuid.uuid1())+'.dcm'
        print(file_name)
        with open(file_name, 'wb+') as temp_file:
            temp_file.write(my_file.read())
        print(file_name)
        ds = dicom.read_file(file_name)
        document = Document()
        document.date_time = datetime.datetime.now()
        document.doc_file = request.FILES['file']
        document.save()
        print(document.doc_id)
        for ke in ds.dir():
            if ke == 'PixelData':
                continue
            prop = DICOMProperty()
            prop.prop_key = ke;
            prop.prop_value = str(getattr(ds, ke, ''))
            prop.doc_id = document
            print(prop)
            prop.save()
        print(Document.objects.all())
        documents = Document.objects.all()
        serializer = DocumentListSerializer(documents)
        print(serializer.data)
        #return Response(status=status.HTTP_200_OK, data=serializer.data)
        return HttpResponseRedirect("/static/header.html")
    
    
    def get(self, request, format=None):
        if request.query_params and 'which' in request.query_params:
            if request.query_params['which'] == 'prop':
                if request.query_params and ('prop_key' in request.query_params) and ('prop_value' in request.query_params):
                    if request.query_params['prop_key'] == 'All' or request.query_params['prop_key'] == 'all':
                        properties = DICOMProperty.objects.filter(prop_value__icontains=request.query_params['prop_value'])
                    else:
                        properties = DICOMProperty.objects.filter(prop_key__icontains=request.query_params['prop_key'], prop_value__icontains=request.query_params['prop_value'])
                    documents = set()
                    for prop in properties:
                        documents.add(prop.doc_id)
                    serializer = DocumentListSerializer(documents)
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
            elif request.query_params['which'] == 'image':
                if request.query_params and request.query_params['prop_key'] and request.query_params['prop_value']:
                    if request.query_params['prop_key'] == 'datetime':
                        documents = Document.objects.filter(date_time__year = request.query_params['prop_value'])
                    else:
                        documents = Document.objects.filter(doc_file__icontains = request.query_params['prop_value'])
                    serializer = DocumentListSerializer(documents)
                    return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            documents = Document.objects.all()
            serializer = DocumentListSerializer(documents)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        
class DocumentDetailView(APIView):
    def get(self, request, format=None):
        if request.query_params and 'doc_id' in request.query_params:
            doc_id = request.query_params['doc_id']
            document = Document.objects.get(doc_id=doc_id)
            serializer = DocumentSerializer(document);
            print(serializer.data)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class PropertiesList(APIView):
    def get(self, request, format=None):
        properties = DICOMProperty.objects.all()
        properties = properties.values('prop_key').distinct()
        serializer = PropertyListSerializer(properties)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    