# coding: utf-8
from django.db import models

class Thread(models.Model):
    """Represents topic"""
    op_post = models.ForeignKey('Post')
    sticky = models.BooleanField(default=False, required=False)
    def __unicode__(self):
        return self.op_post.section+'/'+self.op_post.id

class Post(models.Model):
    """Represents post"""
    section = models.ForeignKey('Section')
    pid = models.PositiveIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    ip = models.IPAddressField()
    deleted = models.BooleanField(required=False)
    poster = models.CharField(max_length=64, required=False)
    tripcode = models.CharField(max_length=64, required=False)
    email = models.CharField(max_length=64, required=False)
    topic = models.CharField(max_length=64, required=False)
    password = models.CharField(max_length=32, required=False)
    file = models.FileField(upload_to=lambda *x: \
        '{.board}/{.thread}/{.pid}'.format(*x), required=False)
    thread = models.ForeignKey('Thread')
    text = models.TextField()
    def __unicode__(self):
        return self.section+'/'+self.id

class FileCategory(models.Model):
    """Category of files"""
    name = models.CharField(max_length=32)
    def __unicode__(self):
        return self.name

class FileType(models.Model):
    """File type"""
    extension = models.CharField(max_length=10, unique=True)
    mime = models.CharField(max_length=250, required=False)
    category = models.ForeignKey('FileCategory')
    def __unicode__(self):
        return self.extension

class Section(models.Model):
    """Board section"""
    slug = models.SlugField(max_length=5)
    name = models.CharField(max_length=64)
    description = models.TextField(required=False)
    filesize_limit = models.PositiveIntegerField(default=5*2**20) # 5mb
    anonymity = models.BooleanField(default=False)
    default_name = models.CharField(max_length=64, default='Anonymous')
    filetypes = models.ManyToManyField(FileCategory)
    bumplimit = models.PositiveSmallIntegerField(default=500)
    threadlimit = models.PositiveSmallIntegerField(default=10)
    group = models.ForeignKey('SectionGroup')
    def __unicode__(self):
        return self.slug

class SectionGroup(models.Model):
    """Group of board sections. Example: [b / d / s] [a / aa] """
    name = models.CharField(max_length=64, required=False)
    order = models.SmallIntegerField()
    def __unicode__(self):
        return self.order

class User(models.Model):
    """User (moderator etc.)"""
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    sections = models.ManyToManyField('Section', required=False) # modded
    def __unicode__(self):
        return self.username