from datetime import datetime, timedelta
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle

class CreateThrottle(BaseThrottle):

    def allow_request(self, request, view):
        ip = request.META.get('REMOTE_ADDR')  # Use the IP address of the user as the key
        cache_key = f"throttle_{ip}_create_project"

        last_request_time = cache.get(cache_key) #  Catch the last request time
        if last_request_time:
            if (datetime.now() - last_request_time).total_seconds() < 5:
                return False  # Do not allow the request

        cache.set(cache_key, datetime.now(), timeout=5)  # Update the last request time
        return True  # Allow the request

    def wait(self):
        return timedelta(seconds=5)  # Wait 10 seconds before allowing the request
