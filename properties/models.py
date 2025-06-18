from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

class Property(models.Model):
    
    PROPERTY_TYPES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
    ]
    
    TRANSACTION_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=8, decimal_places=2, help_text="Area in square meters")
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    main_photo = models.ImageField(upload_to='property_photos/')
    photo1 = models.ImageField(upload_to='property_photos/', blank=True)
    photo2 = models.ImageField(upload_to='property_photos/', blank=True)
    photo3 = models.ImageField(upload_to='property_photos/', blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['-date_created']

class ContactRequest(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    date_sent = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Contact request for {self.property.title}"