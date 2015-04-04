from django import forms
from django.conf import settings
from django.utils.timezone import now
from bambu_blog.models import Post

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = now()
        self.fields['tags'].required = False

        if 'markitup' in settings.INSTALLED_APPS:
            from markitup.widgets import MarkItUpWidget
            self.fields['body'].widget = MarkItUpWidget()
        elif 'grappelli' in settings.INSTALLED_APPS:
            classes = self.fields['css'].widget.attrs.get('class', '').split(' ')
            classes.append('mceNoEditor')
            self.fields['css'].widget.attrs['class'] = ' '.join(set(sorted(classes)))

        self.fields['css'].label = u'Custom CSS'

    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'slug',
            'date',
            'published',
            'body',
            'css',
            'tags',
            'categories'
        )
