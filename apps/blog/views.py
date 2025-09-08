from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer, PostViewSerializer
from .utils import get_client_ip

# class PostListView(ListAPIView):
#     #   Listamos todos los objetos publicados, ya que forma parte de la clase post
#     #   considerar este metodo se implementa
#     queryset = Post.postobjects.all()
#     serializer_class = PostListSerializer

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        #   Obtengo todos los post registrados, de tipo "Published"
        posts = Post.postobjects.all()

        #   Convierto la lista de post en formato JSon
        serialized_post = PostListSerializer(posts, many=True).data

        return Response(serialized_post)


# class PostDetailView(RetrieveAPIView):
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'slug'


class PostDetailView(RetrieveAPIView):
    def get(self, request, slug):
        post = Post.postobjects.get(slug=slug)
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
        post_analytics = PostAnalytics.objects.get(post=post)
        post_analytics.increment_view(request)

        #   Retorno la informacion del post
        return Response(serialized_post)


#   Obtenemos los heading de un determinado post
class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer
    
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter( post__slug = post_slug )