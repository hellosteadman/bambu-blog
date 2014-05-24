Context processor
=================

Bambu Blog has a context processor that will provide a queryset of all the published blog posts. By
design it's supplied as a callable rather than an evaluated query to avoid it being run unnecessarily,
and you should limit the number of returned posts via the ``range`` template tag.

Installation
------------

Add the following to your list of processors::

	bambu_blog.context_processors.latest

Usage
-----

Loop through the latest blog posts in your template like this::

	<ul class="latest-blog-posts">
		{% for post in latest_blog_posts|slice:':3' %}
			<li class="post">
				<a href="{{ post.get_absolute_url }}">{{ post.title }}</a>
			</li>
		{% endfor %}
	</ul>