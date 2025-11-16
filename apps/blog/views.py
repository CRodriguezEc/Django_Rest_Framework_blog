from apps.blog.utils import get_client_ip
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

import redis
from django.conf import settings

#   CACHE
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
#   Libreria para cache manual
from django.core.cache import cache

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, PostViewSerializer

# Importo la clase HasValidAPIKey, ubicada en el directorio "core", en el archivo permissions
from core.permissions import HasValidAPIKey

#   Importo las tarea
from .tasks import increment_post_views_task

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

class PostListView(StandardAPIView):
    #   Valida si el usuario tiene el key de ingreso
    permission_classes = [HasValidAPIKey]
    
    #   Cache por un minuto (60 * 1)
    #   @method_decorator(cache_page(60 * 1))
    def get(self, request, *args, **kwargs):
        try:
            #   Buscamos todos los PostList registrados en cache
            cached_post = cache.get("post_list")
            if cached_post:
                # Registro en redis el post_id del post gestionado
                for post in cached_post:
                    redis_client.incr(f"post:impressions:{post['id']}")
                
                #   Si existen retornamos esta informacion
                # return Response(cached_post)
                return self.paginate(request, cached_post)
            
            #   Obtengo todos los post registrados, de tipo "Published"
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No post found")

            #   En caso que "NO" exista esta información, se realiza el proceso normal de busqueda directo a la DB
            #   Convierto la lista de post en formato JSon
            serialized_post = PostListSerializer(posts, many=True).data
            
            #   Registro esta informacion en cache, 
            #       Clave es "post_list" 
            #       La informacion a registrar es serialized_post, 
            #       Por un tiempo de 1 minuto (60*1)
            cache.set("post_list", serialized_post, timeout=60*1)

            #Registro en redis el post_id del post gestionado
            for post in posts:
                redis_client.incr(f"post:impressions:{post.id}")

        except Exception as e:
            raise APIException(detail=f"An unexpected error occurred PostListView - L042: {str(e)}")

        return self.paginate(request, serialized_post)

class PostDetailView(StandardAPIView):
    #   Valida si el usuario tiene el key de ingreso
    permissions_classes = [HasValidAPIKey]

    def get(self, request, slug):
        ip_address = get_client_ip(request)
        
        try:
            slug = request.query_params.get['slug']
            
            #   Busco en cache por slug en la lista de post, buscabamos todos los post list guardados en cache, 
            #   para este caso el key es PostList. Para el caso de DetailView buscamos en cache todos los post 
            #   cuyo atributo post_detail sea equivalente a la variable slug
            cached_post = cache.get(f"post_detail:{slug}")
            if cached_post:
                #   Incrementa las visitas en 2do plano - ejecutando una tarea de Celery
                increment_post_views_task.delay(cached_post['slug'], ip_address)                
                return self.response(cached_post)
            
            #   Sino esta en cache, obtengo esa informacion desde la DB 
            post = Post.postobjects.get(slug=slug)
            serialized_post = PostSerializer(post).data

            #   Guardo en cache esta información            
            cache.set(f"post_detail:{slug}", serialized_post, timeout= 60 * 5)

            #   Incrementa las vistas en 2do plano - ejecutando una tarea de Celery
            increment_post_views_task.delay(post.slug, ip_address)            
        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exists")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurreed: {str(e)}")

        #   Retorno la informacion del post
        return self.response(serialized_post)

#   Obtenemos los heading de un determinado post
class PostHeadingView(StandardAPIView):
    #   Valida si el usuario tiene el key de ingreso
    permissions_classes = [HasValidAPIKey]
    serializer_class = HeadingSerializer

    def get(self, request):
        post_slug = request.query_params.get("slug")
        heading_objects = Heading.objects.filter(post__slug = post_slug)
        serialized_data = HeadingSerializer(heading_objects, many=True).data

        return self.response(serialized_data)

class IncrementPostClickView(StandardAPIView):
    #   Valida si el usuario tiene el key de ingreso
    permissions_classes = [HasValidAPIKey]

    def post(self, request):
        # Incrementa el contador de cliks de un post basado en slugs
        data = request.data

        try:
            post = Post.postobjects.get( slug = data['slug'] )
        except Post.DoesNotExist:
            raise NotFound(detail="The request post not exist")

        try:
            #   Intenta obtener un objeto "post_analitics" de tipo "post", sino existe creo uno nuevo
            #   la variable "created" es de tipo boolean e indica si el objeto se creo (true) o se encontro (false)
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics:{str(e)}")

        return self.response({
            "message": "Click increment successfully"
            ,   "clicks": post_analytics.clicks
        })