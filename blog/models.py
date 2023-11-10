

from django.db import models
from django.utils import timezone
from django.urls import reverse
from authentication.models  import  CustomUser as User  
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='blog_posts')
    body = models.TextField()
    image = models.ImageField(upload_to='images/', default='post.png')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,  choices=STATUS_CHOICES,  default='draft')

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail_view',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])

    # creating an object for the tag fuction

    tags = TaggableManager()

class Comments(models.Model):


    # The related_name attribute allows you to name the attribute that you use for
    # the relationship from the related object back to this one. After defining this, you
    # can retrieve the post of a comment object using comment.post and retrieve all
    # comments of a post using post.comments.all()

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255,)
    email = models.EmailField()
    body = models.TextField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table ="Comments"
        verbose_name="Comment"
        verbose_name_plural="Comments"
        ordering = ('created',)
    def __str__(self):
        return f'Commented by {self.name} on {self.post}'
