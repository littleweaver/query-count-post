from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)

    # Having side effects in methods and properties is
    # generally not a good idea.
    @property
    def post_count(self):
        return self.blogpost_set.count()


class Blog(models.Model):
    name = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)


class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    blog = models.ForeignKey(Blog, related_name='posts')
    author = models.ForeignKey(Author)
    tags = models.ManyToManyField(Tag, blank=True)
