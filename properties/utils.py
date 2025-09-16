from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Get all properties with low-level cache API.
    Caches the queryset in Redis for 1 hour (3600 seconds).
    """
    # Try to get properties from cache
    properties = cache.get('all_properties')
    
    if properties is None:
        # If not in cache, fetch from database
        properties = list(Property.objects.all())
        
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
        
        print("Properties fetched from database and cached")
    else:
        print("Properties fetched from cache")
    
    return properties