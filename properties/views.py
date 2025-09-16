from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core import serializers
from .models import Property
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with 15-minute caching.
    """
    properties = get_all_properties()
    
    # Convert queryset to list of dictionaries for JSON response
    properties_data = []
    for prop in properties:
        properties_data.append({
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),
            'location': prop.location,
            'created_at': prop.created_at.isoformat()
        })
    
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data)
    })
