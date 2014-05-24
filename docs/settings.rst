Settings
========

``BLOG_COMMENTS_FORM``
	The class of the form used to post comments on a blog entry, expressed as a string (default is
	'bambu_comments.forms.CommentForm')

``BLOG_COMMENTS_MODEL``
	The model used to store and query comments against blog posts. Use the notation supported by
	``django.db.models.loading.get_model`` (default is ``comments.Comment``)

``BLOG_EXCERPT_LENGTH``
	The number of words in a blog excerpt before it'll be truncated (default is 30)

``BLOG_POSTS_PER_PAGE``
	The number of blog posts to display on a page or in a feed (default is 10)

``BLOG_THUMBNAIL_WIDTH``
	The number of pixels wide a featured blog post image should be (default is 640)

``BLOG_XMLRPC_STAFF_ONLY``
	Set to ``True`` to only allow staff users to access the XML-RPC endpoint