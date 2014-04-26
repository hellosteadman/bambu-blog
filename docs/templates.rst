Views and templates
===================

Bambu Blog provides a number of views and templates

Blog index (`/blog/`)
---------------------

The 10 latest blog posts. When the ``page`` querystring argument is set to 2, the 10 published posts
before that are shown, and so on (this pagination is used throughout all of the list views).

Template:
 - ``blog/posts.html``

Blog posts by year (`/blog/2014/`)
----------------------------------

The 10 latest blog posts of the given year.

Templates:
 - ``blog/posts-year.html``
 - ``blog/posts.html``

Blog posts by month (`/blog/2014/04/`)
--------------------------------------

The 10 latest blog posts of the given year and month.

Templates:
 - ``blog/posts-month.html``
 - ``blog/posts-year.html``
 - ``blog/posts.html``

Blog posts by day (`/blog/2014/04/26/`)
---------------------------------------

The 10 latest blog posts of the given year, month and day.

Templates:
 - ``blog/posts-day.html``
 - ``blog/posts-month.html``
 - ``blog/posts-year.html``
 - ``blog/posts.html``

Blog post (`/blog/2014/04/26/slug/`)
------------------------------------

A single blog post, matching a year, month, day and slug.

Template:
 - ``blog/post.html``

Submit blog post comment (`/blog/2014/04/26/slug/comment/`)
-----------------------------------------------------------

A POST-only view that validates then submits a form that allows comments to be posted
to a blog entry. The comment model must have a boolean ``spam`` field and a
``check_for_spam()`` method that takes the HTTP request as its only argument. This
method should return ``True`` or ``False``.

If the form is valid and submission is successful, an ``HttpResponseRedirect`` is returned that
redirects the user back to the blog post page, with a message (via ``django.contrib.messages``).

Template (if submission was unsuccessful):
 - ``blog/post.html``

Blog posts by tag (`/blog/tag/tag-slug/`)
-----------------------------------------

The 10 latest blog posts tagged ``tag-slug``

Templates:
 - ``blog/posts-tag.html``
 - ``blog/posts.html``

Blog posts by category (`/blog/category/category-slug/`)
--------------------------------------------------------

The 10 latest blog posts in the category ``category-slug``

Templates:
 - ``blog/posts-category.html``
 - ``blog/posts.html``

Blog posts by tag (`/blog/author/username/`)
--------------------------------------------

The 10 latest blog posts by the user with the username ``username``.

Templates:
 - ``blog/posts-author.html``
 - ``blog/posts.html``