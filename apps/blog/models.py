from django.db import models

def blog_tumbnail_directory(instance, filename):
    return "blog/{0}/{1}".format( instance.title, filename )

class Post( models.Model ):
    title: models.CharField(max_length=128)
    description: models.CharField(max_length=256)
    content: models.TextField()
    tumbnail: models.ImageField(upload_to='blog_post/')
