from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from django.conf.global_settings import LANGUAGES
from djangoratings.fields import RatingField
from uuslug import uuslug

class Blog(models.Model):
    title=models.CharField(max_length=300, null=True,blank=True)
    owner=models.ForeignKey(User)
    slug=models.SlugField(max_length=350, unique=True)
    overview=models.TextField(null=True,blank=True)
    created_date  = models.DateTimeField(auto_now_add=True,editable=False,default=None,null=True,blank=True)
    lang=models.CharField(max_length=12,null=True,blank=True,default='en',
                          choices=LANGUAGES)
    deleted  = models.BooleanField()
    weight  = models.IntegerField(default=0)
    tags = TaggableManager(blank=True)
    class Meta:
        ordering = ['weight','-created_date']
        #db_table = 'card_collection'
        #app_label = 'blog'
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Blog, self).save(*args, **kwargs)
        """
        try:
            self.slug = slugify(self.title)
            super(Blog, self).save(*args, **kwargs)
        except:
            for i in range(9999999):
                self.slug = slugify("%s_%d"%(self.title,i))
                super(Blog, self).save(*args, **kwargs)
        """        
    def has_edit_permision(self,user):
        if user==self.owner:
            return True
        return False


class Entry(models.Model):
    blog=models.ForeignKey(Blog)
    title=models.CharField(max_length=300, null=True,blank=True)
    author=models.ForeignKey(User)
    slug=models.SlugField(max_length=450,unique=True)
    body=models.TextField(null=True,blank=True)
    published=models.BooleanField()
    deleted  = models.BooleanField()
    lang=models.CharField(max_length=12,null=True,blank=True,default='en',
                          choices=LANGUAGES)
    created_date  = models.DateTimeField(auto_now_add=True,editable=False,default=None,null=True,blank=True)
    translated_from=models.ForeignKey('self',null=True,blank=True)
    tags = TaggableManager(blank=True)
    rating = RatingField(range=5) 
    class Meta:
        ordering = ['-created_date']
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Entry, self).save(*args, **kwargs)
        """
        try:
            self.slug = slugify(self.title)
            super(Entry, self).save(*args, **kwargs)
        except:
            try:
                self.slug = slugify("%s_%s"%(self.blog.title,self.title))
                super(Entry, self).save(*args, **kwargs)
            except:
                for i in range(9999999):
                    self.slug = slugify("%s_%d"%(self.title,i))
                    super(Entry, self).save(*args, **kwargs)
        """
    def get_translations(self):
        return Entry.objects.filter(translated_from=self)
    """
    A list of languages that this entry has no translation for
    """
    def get_non_trans_langs(self):
        trans=Entry.objects.filter(translated_from=self)
        langs =list(LANGUAGES)
        for t in trans:
            try:
                langs=langs.remove(t.lang)
            except:
                print t.lang
        return langs
    
    def has_edit_permision(self,user):
        if user==self.author:
            return True
        return False
    
