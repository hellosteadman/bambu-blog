Cron job and webhook
====================

If you use `Bambu Cron <https://github.com/iamsteadman/bambu-cron>`_
you can install this cron job (just like any other supported by Bambu Cron) to publish blog posts that
are marked with dates in the future. This fires a webhook which you can manage by setting up
`Bambu Webhooks <https://github.com/iamsteadman/bambu-webhooks>`_
to do just about anything you want with it.

In the past this was used to auto-tweet the blog posts, but now I use
`Bambu Buffer <https://github.com/iamsteadman/bambu-buffer>`_
which has its own cron job that figures out what to do with published and unpublished blog posts.

Installation
------------

Once you've installed Bambu Blog, make sure to run ``manage.py cron --setup`` so that Bambu Cron can
pick up the Blog cron job.