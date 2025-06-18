from django import forms
from .models import ContactRequest

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }