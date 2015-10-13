from django.db import models
from django.conf import settings
import datetime

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class State(models.Model):
    name = models.TextField()

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.TextField()
    state = models.ForeignKey(State)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)

    GENDER_CHOICES = (
        ('H', 'Homem'),
        ('M', 'Mulher'),
    )

    # The additional attributes we wish to include.
    display_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='profile_images', default='profile_images/default_avatar.png')
    gender = models.CharField('gender', max_length=1, choices=GENDER_CHOICES)
    creation_date = models.DateTimeField(default=datetime.datetime.now())

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class PublicProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, unique=True)

    # The additional attributes we wish to include.
    job = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    experience = models.TextField(blank=True)
    academics = models.TextField(blank=True)
    tags = models.TextField(blank=True)
    #repositorio


    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class StatusUpdate(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.datetime.now())
    text = models.TextField()

    def __unicode__(self):
        return self.text

class Friendlist(models.Model):
    main_user = models.ForeignKey(User, related_name='main_user', unique=True)
    friends = models.ManyToManyField(User)

    def __unicode__(self):
        return self.main_user.username

class Message(models.Model):
    recipient = models.ForeignKey(User, related_name="recipient")
    sender = models.ForeignKey(User, related_name="sender")
    title = models.CharField(max_length=255, null=True)
    text = models.TextField()
    date = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.text


class Forum(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(_("Description"), blank=True)
    position = models.IntegerField(_("Position"), default=0)

    class Meta:
        ordering = ['position']

    def count_subforuns(self):
        return self.subforuns.count()

    def __unicode__(self):
        return self.name

class SubForum(models.Model):
    forum = models.ForeignKey(Forum,  related_name='subforuns')
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(_("Description"), blank=True)
    position = models.IntegerField(_("Position"), default=0)

    class Meta:
        ordering = ['position']

    def count_categorys(self):
        return self.categorys.count()

    def __unicode__(self):
        return self.name

class Category(models.Model):
    subforum = models.ForeignKey(SubForum,  related_name='categorys')
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(_("Description"), blank=True)
    position = models.IntegerField(_("Position"), default=0)

    class Meta:
        ordering = ['position']



    def count_topics(self):
        return self.topics.count()

        # def get_latest_topic(self):
    #     if self.topics.count() > 0:
    #         return self.topics.all()[0]
    #     return None
    #
    # def get_latest_poster(self):
    #     latest_topic = self.get_latest_topic()
    #     if latest_topic:
    #         return latest_topic.last_post.user.username
    #     return '-'

    # def count_posts(self):
    #     count = 0
    #     for topic in self.topics.all():
    #         count += topic.count_posts()
    #     return count

    def __unicode__(self):
        return self.name

class Topic(models.Model):
    category = models.ForeignKey(Category, related_name='topics')
    last_post = models.ForeignKey('Post', verbose_name=_("Last post"), related_name='forum_last_post', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(_("Name"), max_length=255)
    text = models.TextField()
    views = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    is_closed = models.BooleanField(_("Is closed"), default=False)

    class Meta:
        ordering = ['-last_post__created']

    def count_posts(self):
        return self.posts.count()

    def __unicode__(self):
        return self.title

class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts')
    body = models.TextField(_("Body"))
    views = models.IntegerField(default=0)
    creation_date = models.DateTimeField(default=datetime.datetime.now())
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"), auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='forum_posts')

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.body