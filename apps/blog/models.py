from django.db import models
from django.utils import timezone
import uuid

def blog_tumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format( instance.title, filename )

def category_tumbnail_directory(instance, filename):
    return "blog_categories/{0}/{1}".format(instance.name, filename )

class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    #   Campo padre de la tabla categoria (tabla recursiva)
    parent = models.ForeignKey( "self", related_name="children", on_delete=models.CASCADE, blank=True, null=True )
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
    
    title = models.CharField(max_length=128)
    description= models.CharField(max_length=256)
    content = models.TextField()
    tumbnail = models.ImageField(upload_to='blog_post/')
    
    keywords = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, )
    
    created_at = models.DateTimeField(default=timezone.now)
    
    #   Al momento de editar el post, automaticamente actualiza la fecha de edición del post
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=16
                              , choices = status_options
                              , default= 'draft')
    
    objects = models.Manager() #default manager
    postobjects = postObjects() #custom manager
    
    class Meta:
        ordering = ("-published")
        
    def __str__(self):
        return self.title