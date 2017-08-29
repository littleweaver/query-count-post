import random

from django.db.models import (
    Count,
    F,
    Prefetch,
)
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
    blog = Blog.objects.create(name=' '.join(fake.words(2)))
    Tag.objects.bulk_create((
        Tag(name=' '.join(fake.words(2)))
        for x in range(50)
    ))
    tags = list(Tag.objects.all())
    for x in range(count):
        post = BlogPost.objects.create(
            title=' '.join(fake.words(5)),
            blog=blog,
            author=Author.objects.create(name=fake.name()),
        )
        post.tags = random.sample(tags, random.randint(1, 5))


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


@rollback
def following_m2m():
    create_blog_posts(300)

    with count_queries():
        for blog_post in BlogPost.objects.all():
            print(', '.join((tag.name for tag in blog_post.tags.all())))


@rollback
def following_m2m__prefetch_related():
    create_blog_posts(300)

    with count_queries():
        for blog_post in BlogPost.objects.prefetch_related('tags'):
            print(', '.join((tag.name for tag in blog_post.tags.all())))


@rollback
def following_reverse_fk():
    create_blog_posts(300)

    with count_queries():
        for author in Author.objects.all():
            print(author.name)

            for blog_post in author.blogpost_set.all():
                print(blog_post.title, '||', blog_post.blog.name)


@rollback
def following_reverse_fk__prefetch_related__select_related():
    create_blog_posts(300)

    with count_queries():
        authors = Author.objects.prefetch_related(
            Prefetch(
                'blogpost_set',
                queryset=BlogPost.objects.select_related('blog'),
            )
        )
        for author in authors:
            print(author.name)

            for blog_post in author.blogpost_set.all():
                print(blog_post.title, '||', blog_post.blog.name)


@rollback
def related_object_count():
    create_blog_posts(300)

    with count_queries():
        for author in Author.objects.all():
            print(author.name, '||', author.blogpost_set.count())


@rollback
def related_object_count__annotation():
    create_blog_posts(300)

    with count_queries():
        for author in Author.objects.annotate(blogpost_count=Count('blogpost')):
            print(author.name, '||', author.blogpost_count)


@rollback
def bulk_create():
    blog = Blog.objects.create(name=' '.join(fake.words(2)))
    author = Author.objects.create(name=fake.name())

    with count_queries():
        for x in range(300):
            BlogPost.objects.create(
                title=' '.join(fake.words(5)),
                blog=blog,
                author=author,
            )


@rollback
def bulk_create__bulk_create():
    blog = Blog.objects.create(name=' '.join(fake.words(2)))
    author = Author.objects.create(name=fake.name())

    with count_queries():
        posts = [
            BlogPost(
                title=' '.join(fake.words(5)),
                blog=blog,
                author=author,
            )
            for x in range(300)
        ]
        BlogPost.objects.bulk_create(posts)


@rollback
def update_field_value():
    Blog.objects.create(name=' '.join(fake.words(2)))

    with count_queries():
        blog = Blog.objects.get()
        blog.likes = blog.likes + 1
        blog.save()


@rollback
def update_field_value__f():
    blog = Blog.objects.create(name=' '.join(fake.words(2)))

    with count_queries():
        Blog.objects.filter(
            id=blog.id,
        ).update(
            likes=F('likes') + 1,
        )


@rollback
def reuse_querysets():
    create_blog_posts(1)

    with count_queries():
        if Blog.objects.all():
            print('There are blogs!')
            for blog in Blog.objects.all():
                print(blog.name)


@rollback
def reuse_querysets__reuse():
    create_blog_posts(1)

    with count_queries():
        blogs = Blog.objects.all()
        if blogs:
            print('There are blogs!')
            for blog in blogs:
                print(blog.name)
