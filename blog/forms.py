from django.forms import ModelForm

from blog.models import Blog,Entry

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = (
                  'title',
                  'overview',
                  'tags',
                  'lang'
                  )

class DeleteBlogForm(ModelForm):
    class Meta:
        model = Entry
        fields = (
                  'deleted',
                  )

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = (
                  'title',
                  'body',
                  'tags',
                  'published'
                  )
class EntryDeleteForm(ModelForm):
    class Meta:
        model = Entry
        fields = (
                  'deleted',
                  )
