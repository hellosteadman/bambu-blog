from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now
from taggit.models import Tag
from bambu_blog.models import Category, Post

class BlogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'user',
            password = 'blink',
            email = 'user@example.com'
        )
    
    def tearDown(self):
        self.user.delete()
    
    def test_categories(self):
        category = Category.objects.create(
            name = 'Category name',
            slug = 'category-name'
        )
        
        category.name = 'Category renamed'
        category.save()
        category.delete()
    
    def test_untitled_post(self):
        post = Post.objects.create(
            author = self.user,
            body = 'Something',
            date = now()
        )
        
        post.body = 'Something else'
        post.save()
        post.delete()
    
    def test_titled_post(self):
        post = Post.objects.create(
            title = 'Something',
            slug = 'something',
            author = self.user,
            date = now()
        )
        
        post.title = 'Something else'
        post.save()
        post.delete()
    
    def test_categorised_post(self):
        category = Category.objects.create(
            name = 'Category name',
            slug = 'category-name'
        )
        
        post = Post.objects.create(
            title = 'Something',
            slug = 'something',
            author = self.user,
            date = now()
        )
        
        post.categories.add(category)
        self.assertEqual(Post.objects.filter(categories__slug = 'category-name').count(), 1)
        
        post.categories.remove(category)
        self.assertEqual(Post.objects.filter(categories__slug = 'category-name').count(), 0)
        post.delete()
        category.delete()
    
    def test_tagged_post(self):
        post = Post.objects.create(
            title = 'Something',
            slug = 'something',
            author = self.user,
            date = now()
        )
        
        post.tags.add('tag')
        self.assertEqual(Post.objects.filter(tags__slug = 'tag').count(), 1)
        
        post.tags.remove('tag')
        self.assertEqual(Post.objects.filter(tags__slug = 'tag').count(), 0)
        
        post.delete()
        Tag.objects.get(slug = 'tag').delete()