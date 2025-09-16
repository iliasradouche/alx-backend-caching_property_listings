from django.core.cache import cache
from django_redis import get_redis_connection
import logging
from .models import Property

# Configure logging
logger = logging.getLogger(__name__)

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

def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including hits, misses, and hit ratio.
    """
    try:
        # Connect to Redis via django_redis
        redis_connection = get_redis_connection("default")
        
        # Get Redis INFO statistics
        info = redis_connection.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate total requests and hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0.0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': round(hit_ratio, 4),
            'hit_ratio_percentage': round(hit_ratio * 100, 2)
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, "
                   f"Total={total_requests}, Hit Ratio={hit_ratio:.4f} ({hit_ratio*100:.2f}%)")
        
        print(f"Redis Cache Metrics:")
        print(f"  - Keyspace Hits: {keyspace_hits}")
        print(f"  - Keyspace Misses: {keyspace_misses}")
        print(f"  - Total Requests: {total_requests}")
        print(f"  - Hit Ratio: {hit_ratio:.4f} ({hit_ratio*100:.2f}%)")
        
        return metrics
        
    except Exception as e:
        error_msg = f"Error retrieving Redis cache metrics: {str(e)}"
        logger.error(error_msg)
        print(error_msg)
        
        # Return empty metrics on error
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'hit_ratio_percentage': 0.0,
            'error': str(e)
        }