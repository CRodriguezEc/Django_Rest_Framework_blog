from rest_framework import serializers

from .models import Post, Category, Heading

#   Serializamos la informacion de un post especifico
class PostSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Post
        fields = "__all__"

#   Serializamos la lista de Post registrados en el blog
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [  "id",
                    "title",
                    "description",
                    "tumbnail",
                    "slug",
                    "category",
                    "updated_at" ]

class CategorySerializer( serializers.ModelSerializer ):
    class Meta:
        model = Category
        fields = "__all__"
        
class HeadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            "title",
            "slug",
            "level",
            "order",
        ]