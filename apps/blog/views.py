from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Post, Heading
from .serializers import PostListSerializer, PostSerializer, HeadingSerializer

class PostListView(ListAPIView):
    #   Listamos todos los objetos publicados, ya que forma parte de la clase post
    #   considerar este metodo se implementa
    queryset = Post.postobjects.all()
    serializer_class = PostListSerializer

class PostDetailView(RetrieveAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

#   Obtenemos los heading de un determinado post
class PostHeadingView(ListAPIView):
    serializer_class = HeadingSerializer
    
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        return Heading.objects.filter( post__slug = post_slug )