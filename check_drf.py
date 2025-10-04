# diagnose.py
try:
    from rest_framework.permissions import BasePermission
    print("✓ BasePermission importado correctamente")
except ImportError as e:
    print(f"✗ Error importando BasePermission: {e}")
    
# Verificar qué hay en el módulo permissions
import rest_framework.permissions as perms
print("Atributos disponibles en rest_framework.permissions:")
for attr in dir(perms):
    if not attr.startswith('_'):
        print(f"  - {attr}")