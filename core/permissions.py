import rest_framework.permissions as perms
from django.conf import settings

# class HasValidAPIKey(perms.BasePermission):    
#     def has_permission(self, request):
#         api_key = request.headers.get("API-Key")    
#         return api_key in getattr(settings, "VALID_API_KEYS", [])
    
    
class HasValidAPIKey(perms.BasePermission):
    def has_permission(self, request):
        api_key = request.headers.get("API-Key")
        
        if not api_key:
            return False
        
        # Validación adicional
        if not isinstance(api_key, str) or len(api_key) < 10:
            return False
            
        valid_keys = getattr(settings, "VALID_API_KEYS", [])
        return api_key in valid_keys