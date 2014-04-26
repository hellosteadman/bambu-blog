# Bambu Blog

A simple set of models for a basic blog, with some tools for custom-designed blog post writing

## About Bambu Blog

Bambu Blog was originally intended as a simple blogging tool for web apps, that allowed developers to
quickly setup a blog for their app based on a common Bootstrap template, without needing to manage another
site and set of user accounts. It used Markdown to render text-only copy, and
[Bambu Attachments](https://github.com/iamsteadman/bambu-attachments) to handle uploading images and other
media.

It's grown a little since then, and now supports either the
[MarkItUp](https://bitbucket.org/carljm/django-markitup/src) or
[TinyMCE](https://github.com/aljosa/django-tinymce) editors (just install the Django app you want and
Bambu Blog will detect it and apply the appropriate class names to the main body textbox).

## Installation

Install the package via Pip:

```
pip install bambu-blog
```

Add it to your `INSTALLED_APPS` list:

```python
INSTALLED_APPS = (
    ...
    'bambu.blog'
)
```

Add `bambu.blog.urls` to your URLconf:

```python
urlpatterns = patterns('',
    ...
    url(r'^blog/', include('bambu.blog.urls')),
)
```

## Sync the database

Run `manage.py syncdb` or `manage.py migrate` to setup the database tables.

## Basic usage

The blog uses a number of templates. All of the important ones extend `blog/base.html`, so you should
start by overriding that template to set it up how you like it. The naming convention used throughout the
Bambu collection of apps designates the main content area via the Jinja block `form_content`. A block is
already defined called `sidebar`, so you can either place HTML in there or override `blog/sidebar.inc.html`.

Add a blog post via the admin area of your site. As you're logged in as a staff member you don't have
to publish the blog post to be able to see it on the site once saved. View the blog post index at
/blog/.

Override the `blog/post.html` template to tweak the display of the blog post.

## Todo

* Prepare for internationalisation
* Write more tests

## Documentation

Full documentation can be found at [ReadTheDocs](http://bambu-blog.readthedocs.org/).

## Questions or suggestions?

Find me on Twitter (@[iamsteadman](https://twitter.com/iamsteadman))
or [visit my blog](http://steadman.io/).
