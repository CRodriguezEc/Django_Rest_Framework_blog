import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


def blog_tumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format( instance.title, filename )

def category_tumbnail_directory(instance, filename):
    return "blog_categories/{0}/{1}".format( instance.name, filename )


class Category(models.Model):

    id = models.UUIDField(  primary_key=True
                            , default=uuid.uuid4
                            , editable=False )
    
    #   Campo padre de la tabla categoria (tabla recursiva)
    parent = models.ForeignKey( "self"
                                , related_name="children"
                                , on_delete=models.CASCADE
                                , blank=True
                                , null=True )
    
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    tumbnail = models.ImageField(upload_to=category_tumbnail_directory)
    slug = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name


class Post( models.Model ):
    class postObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter( status='published' )
    
    status_options = (
        ( "draft", "Draft" ),
        ( "published", "Published" )
    )
    
    #   Clave primaria de la tabla Post
    id = models.UUIDField(  primary_key=True
                            , default=uuid.uuid4
                            , editable=False )

    title = models.CharField(max_length=128)
    description= models.CharField(max_length=256)
    # content = models.TextField()  #   Solo caja de texto
    
    #   Asociamos el CKEditor a la caja de texto
    content = RichTextField()       
    tumbnail = models.ImageField(upload_to='blog_post/')
    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, )
    created_at = models.DateTimeField(default=timezone.now)
    
    #   Al momento de editar el post, automaticamente actualiza la fecha de edición del post
    updated_at = models.DateTimeField(auto_now=True)
    
    #   Contador de visitas a un determinado "post"
    #   intNumVisitas = models.IntegerField( default = 0 )

    status = models.CharField(  max_length=16
                                , choices = status_options
                                , default= 'draft' )
    
    #default manager
    objects = models.Manager()

    #custom manager
    postobjects = postObjects() 
    
    class Meta:
        ordering = ("status", "-created_at")
    
    def __str__(self):
        return self.title

class PostView(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)    
    post = models.ForeignKey(Post, on_delete = models.PROTECT, related_name = 'post_view',)    
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

#   Permite la navegabilidad dentro del contenido del blog (usabilidad tipo menu)
class Heading( models.Model ):
    #   Clave primaria de la tabla Heading
    id = models.UUIDField(  primary_key=True
                            , default=uuid.uuid4
                            , editable=False )
    
    post = models.ForeignKey(   Post
                                ,   on_delete=models.PROTECT
                                ,   related_name='headings' )
    
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    #   Admite numeros positivos / negativos
    level = models.IntegerField(
        choices=(   (1, "H1"),
                    (2, "H2"),
                    (3, "H3"),
                    (4, "H4"),
                    (5, "H5"),
                    (6, "H6") )
    )

    #   Admite solo valores positivos
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order",]

    def save(self, *args, **kwargs):
        if not self.slug:
            #   Elimina los espacios en blanco en una cadena y los reemplaza por guiones, 
            #   p.e.: "casa de lola" a "casa-de-lola"
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)



