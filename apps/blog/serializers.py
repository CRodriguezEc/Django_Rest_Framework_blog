from rest_framework import serializers
from .models import Post, Category, Heading

#   Serializamos la informacion de las categorias y serializamos todos sus campos
class CategorySerializer( serializers.ModelSerializer ):
    class Meta:
        model = Category
        fields = "__all__"

        
#   Serializamos la informacion de las categorias y serializamos los campos determinados
class CategoryListSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [  "title",
                    "slug",
                    "level",
                    "order", ]


#   Serializamos la informacion de un post especifico
class PostSerializer( serializers.ModelSerializer ):
    category = CategorySerializer()
    headings = HeadingSerializer ( many = True )
    
    class Meta:
        model = Post
        fields = "__all__"


#   Serializamos la lista de Post registrados en el blog
class PostListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    class Meta:
        model = Post
        fields = [  "id",
                    "title",
                    "description",
                    "tumbnail",
                    "slug",
                    "category",
                    "updated_at" ]

