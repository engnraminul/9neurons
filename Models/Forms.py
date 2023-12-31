from django import forms
from .models import Model, Files, Category, Sub_Category
from ckeditor.widgets import CKEditorWidget

class ModelFilesForm(forms.ModelForm):
    file = forms.FileField(required=False)  # Custom form field for the file
    
    class Meta:
        model = Model
        fields = ['title', 'category', 'sub_category', 'content',]

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = ['title', 'category', 'sub_category', 'content',]
