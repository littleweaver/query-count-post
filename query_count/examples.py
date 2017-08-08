from faker import Faker

from query_count.models import (
    Author,
    Blog,
    BlogPost,
    Tag,
)
from query_count.decorators import (
    count_queries,
    rollback,
)

__all__ = (
    'following_foreignkeys__small', 'following_foreignkeys__small__select_related',
    'following_foreignkeys__large', 'following_foreignkeys__large__select_related',
)


fake = Faker()


def create_blog_posts(count):
    blog = Blog.objects.create(name=fake.words(2))
    for x in range(count):
        BlogPost.objects.create(
            title=fake.words(5),
            blog=blog,
            author=Author.objects.create(name=fake.name()),
        )


# Rollback and count_queries are small utility decorators that ensure
# a clean database while still tracking how many queries are executed
# at critical steps.
@rollback
def following_foreignkeys__small():
    create_blog_posts(1)

    with count_queries():
        blog_post = BlogPost.objects.get()
        print(blog_post.author.name)


@rollback
def following_foreignkeys__small__select_related():
    create_blog_posts(1)

    with count_queries():
        blog_post = BlogPost.objects.select_related('author').get()
        print(blog_post.author.name)


@rollback
def following_foreignkeys__large():
    create_blog_posts(300)

    with count_queries():
        for blog_post in BlogPost.objects.all():
            print(blog_post.author.name)


@rollback
def following_foreignkeys__large__select_related():
    create_blog_posts(300)

    with count_queries():
        for blog_post in BlogPost.objects.select_related('author'):
            print(blog_post.author.name)
