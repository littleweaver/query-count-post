from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag, blank=True)
