from django.db import models
from django.core.files.storage import default_storage

# Create your models here.

class Document(models.Model):
    doc_id = models.AutoField(primary_key=True)
    doc_file = models.FileField(upload_to='')
    date_time = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.doc_file.name
    

class DICOMProperty(models.Model):
    prop_id = models.AutoField(primary_key=True)
    prop_key = models.TextField(max_length = 500)
    prop_value = models.TextField(max_length = 500)
    doc_id = models.ForeignKey(Document, related_name='properties')
    
    def __unicode__(self):
        return str(self.prop_key) +" => "+ str(self.prop_value) 