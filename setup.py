from setuptools import setup, find_packages

setup(
    name='query_count',
    version="0.0",
    description="Query count demo app",
    author='Little Weaver',
    author_email='hello@littleweaverweb.com',
    url='https://github.com/littleweaver/query-count-post',
    packages=find_packages(),
    package_data={'': ["*.*"]},
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django'
    ],
)
