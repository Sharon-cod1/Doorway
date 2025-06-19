from django import forms
from .models import ContactRequest, Property

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'property_type', 'transaction_type', 
                 'price', 'bedrooms', 'bathrooms', 'area', 'location', 
                 'city', 'address', 'main_photo', 'photo1', 'photo2', 'photo3']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }