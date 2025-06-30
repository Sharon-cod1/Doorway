from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

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
    is_published = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

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
        return f"{self.name} - {self.property.title}"
    
User = get_user_model()

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., 'view', 'like'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.interaction_type} - {self.property.title}"