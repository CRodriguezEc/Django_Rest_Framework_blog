# Build paths inside the project like this: BASE_DIR / 'subdir'.
import environ
import os
from pathlib import Path
from django.conf import settings

# from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import HasValidAPIKey


BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, 'app/core/.env'))

print("<<<<<<<<<<<")
print( os.path.join(BASE_DIR, 'app/core/.env') )
print( str("dixesJWR5a07MqGyRNC04KFTXKeIB78zgZivtN43T0ZY0RwtRy0e4VTOTgYZe7n7JWRQjqO3vqe6IDmZBkzZGd2qfeAu8rEaECHLeryOq32N1com1sxvUPae1BsM0hDD").split(",") )
print( env.str("VALID_API_KEYS").split(",") )

#   Valida si el usuario tiene el key de ingreso
permissions_classes = [HasValidAPIKey.has_permission]
print(permissions_classes)

print(">>>>>>>>>>>")