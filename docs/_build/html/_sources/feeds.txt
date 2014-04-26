Feeds
=====

Of course Bambu Blog exposes RSS feeds. It uses similar URL patterns to those found in well-configured
WordPress sites, with lots of URLs suffixed with `/feed/` (for example, the blog index, category views,
author views, etc).

Blog index (`/blog/feed/`)
--------------------------

The 10 latest blog posts. When the ``page`` querystring argument is set to 2, the 10 published posts
before that are shown, and so on (this pagination is used throughout all of the feeds).

Blog posts by year (`/blog/2014/feed/`)
---------------------------------------

The 10 latest blog posts of the given year (mainly provided to conform to WordPress' URL conventions).

Blog posts by month (`/blog/2014/04/feed/`)
-------------------------------------------

The 10 latest blog posts of the given year and month (mainly provided to conform to WordPress' URL
conventions).

Blog posts by day (`/blog/2014/04/26/feed/`)
--------------------------------------------

The 10 latest blog posts of the given year, month and day (mainly provided to conform to WordPress' URL
conventions).

Blog posts by tag (`/blog/tag/tag-slug/feed/`)
----------------------------------------------

The 10 latest blog posts tagged ``tag-slug``

Blog posts by category (`/blog/category/category-slug/feed/`)
-------------------------------------------------------------

The 10 latest blog posts in the category ``category-slug``

Blog posts by tag (`/blog/author/username/feed/`)
-------------------------------------------------

The 10 latest blog posts by the user with the username ``username``.