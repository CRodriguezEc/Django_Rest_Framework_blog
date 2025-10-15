from django.test import TestCase
# Create your tests here.

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
            name = "Tech"
            ,   title = "Technology"
            ,   description = "All about technology"
            ,   slug="tech" )
        
        #   Creo un post, e instancio la categoria recordando que esta es clave foranea de categoria
        self.post = Post.objects.create(
            title = "Post 1"
            ,   description = "A test post"
            ,   content = "Content for the post"
            ,   thumbnail = None
            ,   keywords = "test, post"
            ,   slug = "post-1"
            ,   category = self.category
            ,   status = "published"
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
        