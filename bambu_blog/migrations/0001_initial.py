# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('blog_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('bambu_blog', ['Category'])

        # Adding model 'Post'
        db.create_table('blog_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='blog_posts', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('broadcast', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('excerpt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('css', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('bambu_blog', ['Post'])

        # Adding M2M table for field categories on 'Post'
        m2m_table_name = db.shorten_name('blog_post_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['bambu_blog.post'], null=False)),
            ('category', models.ForeignKey(orm['bambu_blog.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'category_id'])

        # Adding model 'PostUpload'
        db.create_table('blog_post_upload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('mimetype', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
        ))
        db.send_create_signal('bambu_blog', ['PostUpload'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('blog_category')

        # Deleting model 'Post'
        db.delete_table('blog_post')

        # Removing M2M table for field categories on 'Post'
        db.delete_table(db.shorten_name('blog_post_categories'))

        # Deleting model 'PostUpload'
        db.delete_table('blog_post_upload')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bambu_blog.category': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Category', 'db_table': "'blog_category'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'bambu_blog.post': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Post', 'db_table': "'blog_post'"},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blog_posts'", 'to': u"orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'broadcast': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['bambu_blog.Category']"}),
            'css': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'excerpt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'bambu_blog.postupload': {
            'Meta': {'object_name': 'PostUpload', 'db_table': "'blog_post_upload'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bambu_blog']