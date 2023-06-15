from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.
from django.db.models.fields import related


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    e_mail_address = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.caption}"


class Post(models.Model):
    title = models.CharField(max_length=50)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="posts", null=True, )
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True, )
    content = models.TextField(validators=[MinLengthValidator(10)])
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag, )

    def __str__(self):
        return f"{self.title} By {self.author}"


class Comments(models.Model):
    user_name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.TextField(max_length=250, )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
