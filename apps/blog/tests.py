from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.conf import settings

from .models import Category, Post, PostAnalytics, Heading

#   Test para el modelo category
class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name = "Tech"
            ,   title = "Technology"
            ,   description = "All about technology"
            ,   slug="tech" )
        
    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Tech')
        self.assertEqual(self.category.title, 'Technology')
        
#   Test para el modelo "post"
class PostModelTest(TestCase):
    def setUp(self):
        #   Creo una categoria
        self.category = Category.objects.create(
            name="Tech"
            ,   title="Technology"
            ,   description="All about technology"
            ,   slug="tech" )
        
        #   Creo un post, e instancio la categoria recordando que esta es clave foranea de categoria
        self.post = Post.objects.create(
            title="Post 1"
            ,   description="A test post"
            ,   content="Content for the post"
            ,   thumbnail=None
            ,   keywords="test, post"
            ,   slug="post-1"
            ,   category=self.category
            ,   status="published"
        )
        
    def test_post_creation(self):
        self.assertEqual(str(self.post), "Post 1")
        self.assertEqual(self.post.category.name, "Tech")

    def test_post_published_manager(self):
        self.assertTrue(Post.postobjects.filter(status="published").exists())
            
#   Test para el modelo PostAnalytics
class PostAnalyticsModelTest(TestCase):
    def setUp(self):
        #   Creo una categoria
        self.category = Category.objects.create(
            name = "Analytics"
            ,   slug="analytics" )
        
        #   Creo un post
        self.post = Post.objects.create(
            title="Analytics Post"
            ,   description="Post for analytics"
            ,   content="Analytics content"
            ,   slug="analytics-post"
            ,   category=self.category )
        
        #   Creo un postAnalytics
        self.analytics = PostAnalytics.objects.create(post=self.post)
        
    def test_click_through_rate_update(self):
        self.analytics.increment_impressions()
        self.analytics.increment_click()
        self.analytics.refresh_from_db()
        self.assertEqual(self.analytics.click_through_rate, 100.0)
        
        
#   Test para el modelo Heading
class HeadingModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Heading"
                                                ,   slug = "Heading" )

        self.post = Post.objects.create(
            title = "Post with headings"
            ,   description = "Post containing headings"
            ,   content="Content with headings"
            ,   slug="post-with-headings"
            ,   category=self.category
        )
        
        self.heading = Heading.objects.create(
            post = self.post
            ,   title = "Heading 1"
            ,   slug = "heading-1"
            ,   level = 1
            ,   order = 1
        )
        
    def test_heading_creation(self):
        self.assertEqual(self.heading.slug, "heading-1")
        self.assertEqual(self.heading.level, 1)
            

######################
#   VIEW TEST
######################

class PostListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.category = Category.objects.create(name="API"
                                                ,   slug = "api" )

        self.api_key = settings.VALID_API_KEYS[0]
        self.post = Post.objects.create(
            title="API Post"
            ,   description="API post - description"
            ,   content="API Content"
            ,   slug="api-post"
            ,   category=self.category
            ,   status="published"
        )
        
    def test_get_post_list(self):
        #   Hacemos uso del metodo "reverse" el cual es un metodo propio de django 
        #   el cual identifica una determinada "url" mediante el atributo "name" de 
        #   cada uno de las urlpatterns registrados en el archivo urls.py de nuestro app
        url = reverse('post-list')
        
        # Llamamos a la url
        response = self.client.get( url
                                    ,   HTTP_API_KEY=self.api_key )
        
        data = response.json()
        
        # self.assertIn('success', data)
        # self.assertTrue(data['success'])        
        # self.assertIn('status', data)
        # self.assertEqual(data['status'], 200)
        # self.assertIn('results', data)
        # self.assertEqual(data['count'], 1)
        # results = data['results']
        # self.assertEqual(len(results), 1)
        print(data)
        
        
        
        
        
        

