from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Property
from .forms import ContactForm

class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True)
        
        # Filter by transaction type (sale/rent)
        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type in ['sale', 'rent']:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by property type
        property_type = self.request.GET.get('property_type')
        if property_type in ['house', 'apartment', 'land', 'commercial']:
            queryset = queryset.filter(property_type=property_type)
        
        # Filter by city
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)
        
        # Filter by bedrooms
        bedrooms = self.request.GET.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms=bedrooms)
        
        return queryset.order_by('-date_created')

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

def home(request):
    featured_properties = Property.objects.filter(is_featured=True, is_published=True).order_by('-date_created')[:6]
    recent_properties = Property.objects.filter(is_published=True).order_by('-date_created')[:6]
    
    context = {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
    }
    return render(request, 'properties/home.html', context)

def about(request):
    return render(request, 'properties/about.html')

def contact(request):
    return render(request, 'properties/contact.html')