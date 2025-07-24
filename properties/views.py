from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Property
from .forms import ContactForm, PropertyForm
from .recommendations import get_recommendations    


# List view for all published properties with filtering
class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 9

    def get_queryset(self):
        queryset = Property.objects.filter(is_published=True)

        # Filter by transaction type (sale or rent)
        transaction_type = self.request.GET.get('transaction_type')
        if transaction_type in ['sale', 'rent']:
            queryset = queryset.filter(transaction_type=transaction_type)

        # Filter by property type (house, apartment, land, commercial)
        property_type = self.request.GET.get('property_type')
        if property_type in ['house', 'apartment', 'land', 'commercial']:
            queryset = queryset.filter(property_type=property_type)

        # Filter by city
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__iexact=city)

        # Filter by number of bedrooms
        bedrooms = self.request.GET.get('bedrooms')
        if bedrooms and bedrooms.isdigit():
            queryset = queryset.filter(bedrooms=int(bedrooms))

        return queryset.order_by('-date_created')


# Detail view for a single property
class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()  # Form for sending inquiry
        return context


# Home page view
def home(request):
    featured_properties = Property.objects.filter(is_featured=True, is_published=True).order_by('-date_created')[:6]
    recent_properties = Property.objects.filter(is_published=True).order_by('-date_created')[:6]

    context = {
        'featured_properties': featured_properties,
        'recent_properties': recent_properties,
    }
    return render(request, 'properties/home.html', context)


# Static about page
def about(request):
    return render(request, 'properties/about.html')


# Static contact page
def contact(request):
    return render(request, 'properties/contact.html')


# Dashboard view: shows logged-in user's properties
@login_required
def dashboard(request):
    user_properties = request.user.properties.all()
    return render(request, 'properties/dashboard.html', {'properties': user_properties})


# Add new property (only for logged-in users)
@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('dashboard')
    else:
        form = PropertyForm()
    return render(request, 'properties/add_property.html', {'form': form})


# Edit existing property (only by owner)
@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/edit_property.html', {'form': form})

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)

    # Get similar properties: same city and same property type, excluding current one
    similar_properties = Property.objects.filter(
        city=property.city,
        property_type=property.property_type,
        is_published=True
    ).exclude(pk=property.pk)[:4]

    recommendations = get_recommendations(request.user.id) if request.user.is_authenticated else []

    return render(request, 'property_detail.html', {
        'property': property,
        'recommendations': recommendations,
        'similar_properties': similar_properties
    })
