from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException

import redis
from django.conf import settings

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, PostViewSerializer
from .utils import get_client_ip
from .tasks import increment_post_impressions

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

# class PostListView(ListAPIView):
#     #   Listamos todos los objetos publicados, ya que forma parte de la clase post
#     #   considerar este metodo se implementa
#     queryset = Post.postobjects.all()
#     serializer_class = PostListSerializer

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            #   Obtengo todos los post registrados, de tipo "Published"
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail="No post found")
            
            #   Convierto la lista de post en formato JSon
            serialized_post = PostListSerializer(posts, many=True).data
            
            for post in posts:
                redis_client.incr(f"post:impressions:{post.id}")
                
            serialized_post = PostListSerializer(post, many=True).data
            
        except Post.DoesNotExist:
            raise NotFound(detail="No post found.")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurred: {str(e)}")

        return Response(serialized_post)


# class PostDetailView(RetrieveAPIView):
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'slug'


class PostDetailView(RetrieveAPIView):
    def get(self, request, slug):
        try:
            post = Post.postobjects.get(slug=slug)
        except Post.DoesNotExist:
            raise NotFound(detail="The requested post does not exists")
        except Exception as e:
            raise APIException(detail=f"An unexpected error ocurreed: {str(e)}")
        
        serialized_post = PostSerializer(post).data
        
        #
        #   Version contador de visitas
        #
        # # Obtengo la direccion IP del usuario
        # client_ip = get_client_ip(request)

        # #   Verifico si el el post revisado por el usuario fue contabilizado
        # #   Sí, ya fue registrado retorno la misma misma informacion del post
        # if PostView.objects.filter(post=post, ip_address=client_ip).exists():
        #     return Response(serialized_post)

        # # Sino fue registrado lo cuento
        # PostView.objects.create(post=post, ip_address=client_ip)

        #
        #   Gestiona el control de visitas desde la opcion "Analitica"
        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.increment_view(request)
        except PostAnalytics.DoesNotExist:
            raise NotFound(detail="Analytics data for this post does not exists")
        except Exception as e:
            raise APIException(detail=f"An error ocurred while updating post analytics:---> {str(e)}")

        #   Retorno la informacion del post
        return Response(serialized_post)


#   Obtenemos los heading de un determinado post
class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer
    
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter( post__slug = post_slug )
    
    
class IncrementPostClickView(APIView):
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
            raise APIException(detail=f"An error ocurred while updating post analytics:>>>>> {str(e)}")
        
        return Response({
            "message": "Click increment successfully"
            ,   "clicks": post_analytics.clicks
        })